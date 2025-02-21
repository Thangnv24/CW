import abc
import itertools
import typing
from dataclasses import dataclass
from llvmlite.ir import FunctionType
from .table import *
from llvmlite import binding
from .pointer import *
import enum
from llvmlite import ir

# # define classes that represent data types
# # определить классы, представляющие типы данных
# # -*- coding: utf-8 -*-


################################################################################
# Lớp cơ sở đại diện cho kiểu dữ liệu
# Base class representing data types
################################################################################
class Type:
    """Lớp cơ sở cho tất cả các kiểu dữ liệu trong trình biên dịch
    Base class for all compiler data types"""
    name = "undefined"
    mangle_suff = "Und"

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __ne__(self, other):
        return not self.__eq__(other)

    def default_value(self):
        return None

    def castable_to(self, other_type):
        raise NotImplementedError()

    def cast_to(self, other_type, builder: ir.IRBuilder):
        raise NotImplementedError()

    def __str__(self):
        return "Auto"

    def llvm_type(self):
        pass

################################################################################
# Các kiểu dữ liệu nguyên thủy
# Primitive data types
################################################################################
class VoidT(Type):
    """Đại diện cho kiểu void (không có giá trị)
        Represents void type (no value)"""
    name = "void"
    mangle_name = ""

    def __str__(self):
        return "void"

    def castable_to(self, other_type):
        return True

    def llvm_type(self) -> ir.VoidType:
        return ir.VoidType()


class NumericT(Type):
    """Lớp cơ sở cho các kiểu số
        Base class for numeric types"""
    name = "numeric"
    mangle_suff = "N"
    priority = 0

    def default_value(self):
        return 0

    def castable_to(self, other_type):
        return isinstance(other_type, NumericT) and self.priority <= other_type.priority

    def cmp(self, op, builder: ir.IRBuilder, name: str = None):
        raise NotImplementedError("Compare Numeric")

    def add(self, builder: ir.IRBuilder, name: str = None):
        raise NotImplementedError("Addition Numeric")

    def sub(self, builder: ir.IRBuilder, name: str = None):
        raise NotImplementedError("Subtraction Numeric")

    def mul(self, builder: ir.IRBuilder, name: str = None):
        raise NotImplementedError("Multiplication  Numeric")

    def div(self, builder: ir.IRBuilder, name: str = None):
        raise NotImplementedError("Division Numeric")

    def neg(self, builder: ir.IRBuilder, name: str = None):
        raise NotImplementedError("Negation Numeric")


class IntegralT(NumericT):
    """Kiểu số nguyên (cơ sở cho các kiểu nguyên cụ thể)
            Base integral type (for specific integer types)"""
    name = "integral"
    mangle_suff = "N"
    priority = 0

    def cast_to(self, other_type, builder: ir.IRBuilder):
        if isinstance(other_type, IntegralT):
            return lambda x: builder.zext(x, other_type.llvm_type())
        elif isinstance(other_type, FloatingPointT):
            return lambda x: builder.sitofp(x, other_type.llvm_type())
        else:
            return None

    def cmp(self, op, builder: ir.IRBuilder, name: str = None):
        op = "!=" if op == "<>" else op
        op = "==" if op == "=" else op
        return lambda lhs, rhs: builder.icmp_signed(op, lhs, rhs, name if name else '')

    def add(self, builder: ir.IRBuilder, name: str = None):
        return lambda lhs, rhs: builder.add(lhs, rhs, name if name else '')

    def sub(self, builder: ir.IRBuilder, name: str = None):
        return lambda lhs, rhs: builder.sub(lhs, rhs, name if name else '')

    def mul(self, builder: ir.IRBuilder, name: str = None):
        return lambda lhs, rhs: builder.mul(lhs, rhs, name if name else '')

    def div(self, builder: ir.IRBuilder, name: str = None):
        return lambda lhs, rhs: builder.sdiv(lhs, rhs, name if name else '')

    def neg(self, builder: ir.IRBuilder, name: str = None):
        return lambda lhs: builder.neg(lhs, name if name else '')


class FloatingPointT(NumericT):
    """Kiểu số thực (cơ sở cho các kiểu dấu phẩy động)
        Base floating-point type"""

    name = "floating_point"
    mangle_suff = "N"
    priority = 0

    def cast_to(self, other_type, builder: ir.IRBuilder):
        if isinstance(other_type, FloatingPointT):
            return lambda x: builder.fpext(x, other_type.llvm_type())
        else:
            return None

    def cmp(self, op, builder: ir.IRBuilder, name: str = None):
        op = "!=" if op == "<>" else op
        op = "==" if op == "=" else op
        return lambda lhs, rhs: builder.fcmp_ordered(op, lhs, rhs, name if name else '')

    def add(self, builder: ir.IRBuilder, name: str = None):
        return lambda lhs, rhs: builder.fadd(lhs, rhs, name if name else '')

    def sub(self, builder: ir.IRBuilder, name: str = None):
        return lambda lhs, rhs: builder.fsub(lhs, rhs, name if name else '')

    def mul(self, builder: ir.IRBuilder, name: str = None):
        return lambda lhs, rhs: builder.fmul(lhs, rhs, name if name else '')

    def div(self, builder: ir.IRBuilder, name: str = None):
        return lambda lhs, rhs: builder.fdiv(lhs, rhs, name if name else '')

    def neg(self, builder: ir.IRBuilder, name: str = None):
        return lambda lhs: builder.fneg(lhs, name if name else '')


class BoolT(IntegralT):
    """Kiểu boolean (true/false)
        Boolean type (true/false)"""
    name = "bool"
    mangle_suff = "B"
    priority = 1

    def __str__(self):
        return "Bool"

    def llvm_type(self):
        return ir.IntType(8)


class IntegerT(IntegralT):
    """Kiểu số nguyên 32-bit
        32-bit integer type"""
    name = "%"
    mangle_suff = "I"
    priority = 2

    def __str__(self):
        return "Integer"

    def llvm_type(self):
        return ir.IntType(32)


class LongT(IntegralT):
    """Kiểu số nguyên 64-bit
    64-bit long integer type"""
    name = "&"
    mangle_suff = "L"
    priority = 3

    def __str__(self):
        return "Long"

    def llvm_type(self):
        return ir.IntType(64)


class FloatT(FloatingPointT):
    """Kiểu số thực chính xác đơn (32-bit)
    32-bit single-precision floating-point type"""
    name = "!"
    mangle_suff = "F"
    priority = 4

    def __str__(self):
        return "Float"

    def llvm_type(self):
        return ir.FloatType()


class DoubleT(FloatingPointT):
    """Kiểu số thực chính xác kép (64-bit)
        64-bit double-precision floating-point type"""
    name = "#"
    mangle_suff = "D"
    priority = 5

    def __str__(self):
        return "Double"

    def llvm_type(self):
        return ir.DoubleType()


class StringT(Type):
    """Kiểu chuỗi ký tự Unicode
        Unicode string type"""
    name = "$"
    mangle_suff = "S"
    priority = 0

    def __init__(self, is_const:bool = False, len:int = 0):
        super().__init__()
        self.is_const = is_const
        self.len = len


    def __str__(self):
        return "String"

    def default_value(self):
        if self.is_const:
            return bytearray([0] * ((self.len + 1) * 4))
        else:
            return None

    def castable_to(self, other_type):
        return isinstance(other_type, StringT)

    def cast_to(self, other_type, builder: ir.IRBuilder):
        pass

    def llvm_type(self):
        if self.is_const:
            return ir.ArrayType(ir.IntType(32), self.len + 1)
        else:
            return ir.PointerType(ir.IntType(32))


class ArrayT(Type):
    """Kiểu mảng đa chiều
        Multi-dimensional array type"""
    name = "array"

    def __init__(self, valueT:Type, size: list[int], is_function_param: bool = False):
        self.type = valueT
        self.size = size
        self.mangle_suff = "A" + valueT.mangle_suff * len(size)
        self.is_function_param = is_function_param

    def __eq__(self, other):
        if isinstance(other, ArrayT):
            self_any = self.type == Type()
            other_any = other.type == Type()
            if self_any or other_any:
                return self.size == other.size if len(self.size) != 1 and len(other.size) != 1 else True
            if isinstance(self.size[0], int) and isinstance(other.size[0], int) and self.is_function_param == other.is_function_param:
                return self.type == other.type and self.size == other.size
            else:
                return self.type == other.type and len(self.size) == len(other.size)
        return False

    def __str__(self):
        return f"{self.type}[]"

    def default_value(self):
        sz = self.size[0] if not hasattr(self.size[0], "value") else self.size[0].value
        if len(self.size) == 1:
            return [0] * sz
        elif len(self.size) >= 1:
            return [ArrayT(self.type, self.size[1:]).default_value()] * sz


    def llvm_type(self):
        if self.is_function_param:
            return self.llvm_type_ref()
        else:
            return self.llvm_type_init()

    def llvm_type_init(self):
        if len(self.size) == 1:
            return ir.ArrayType(self.type.llvm_type(), self.size[0])
        elif len(self.size) >= 1:
            return ir.ArrayType(ArrayT(self.type, self.size[1:]).llvm_type_init(), self.size[0])

    def llvm_type_ref(self):
        if len(self.size) == 1:
            return ir.PointerType(self.type.llvm_type(), self.size[0])
        elif len(self.size) >= 1:
            return ir.PointerType(ArrayT(self.type, self.size[1:]).llvm_type_ref(), self.size[0])

    def cast_to(self, other_type, builder: ir.IRBuilder):
        def casting(lhs_val_list, rhs_val_list):
            result = []
            for lhs_val, rhs_val in zip(lhs_val_list, rhs_val_list):
                result.append(self.type.cast_to(other_type, builder)(lhs_val, rhs_val))
            return result
        return casting

    def castable_to(self, other_type):
        return self.size == other_type.size and self.type == other_type.type


class VarArguT(Type):
    """Kiểu tham số biến đổi (variadic arguments)
        Variadic arguments type"""
    name = "..."

    def __str__(self):
        return self.name


class FunctionT(Type):
    """Kiểu hàm (procedure)
        Function/procedure type"""
    name = "proc"

    def __init__(self, retT: Type, argsT: list[Type]):
        self.retT = retT
        self.argsT = argsT

    def __eq__(self, other):
        if isinstance(other, FunctionT):
            va_lhs = sum(1 if isinstance(arg, VarArguT) else 0 for arg in self.argsT)
            va_rhs = sum(1 if isinstance(arg, VarArguT) else 0 for arg in other.argsT)
            if va_lhs > 0 or va_rhs > 0:
                result = True
                for idx in range(min(len(self.argsT), len(other.argsT))):
                    if isinstance(self.argsT[idx],  VarArguT) or isinstance(other.argsT[idx],  VarArguT):
                        return result
                    result &= self.argsT[idx] == other.argsT[idx]
                return result
            else:
                result = self.retT == other.retT and len(self.argsT) == len(other.argsT)
                return result and all([self.argsT[i] == other.argsT[i] for i in range(len(self.argsT))])
        return False

    def __str__(self):
        return f"{self.retT}(" + ','.join([str(v) for v in self.argsT]) + ")"

    def castable_to(self, other_type):
        result = self.retT == other_type.retT and len(self.argsT) == len(other_type.argsT)
        if not result:
            return False
        for idx in range(len(self.argsT)):
            result &= self.argsT[idx].castable_to(other_type.argsT[idx])
        return result

################################################################################
# Kiểu vòng lặp
# Loop type enumeration
################################################################################
class WhileT(enum.Enum):
    """Các loại vòng lặp được hỗ trợ
        Supported loop types"""
    PreUntil = 0
    PreWhile = 1
    Endless = 2
    PostUntil = 3
    PostWhile = 5


class Expr(abc.ABC):
    def __init__(self):
        self.type = Type()

    def relax(self, symbol_table: ScopeManager, lvalue=True):
        return self

    def constant_propagation(self):
        return self

    def Gen(self, symbol_table: ScopeManager, lvalue: bool = True):
        return self


class Statement(abc.ABC):

    def constant_propagation(self):
        return self

    def Gen(self, symbol_table: ScopeManager):
        return self


@dataclass
class Varname:
    pos: pe.Position
    name: str
    type: Type

    @pe.ExAction
    def create(attrs, coords, res_coord):
        varname, type = attrs
        cvarname, ctype = coords
        return Varname(cvarname, varname, type)

    def __eq__(self, other):
        if isinstance(other, Varname):
            return self.name == other.name and self.type == other.type
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def mangle_str(self):
        if len(self.type.name) == 1 or self.type.name == 'String':
            return f"{self.name}{self.type.mangle_suff}"

    def __str__(self):
        if len(self.type.name) == 1 or self.type.name == 'String':
            return f"{self.name}{self.type.name}"
        else:
            return f"{self.type} {self.name}"


@dataclass
class Constant_expression(Expr):
    pos: pe.Position
    value: typing.Any
    type: Type

    @pe.ExAction
    def createInt(attrs, coords, res_coord):
        value = attrs[0]
        cvalue = coords[0]
        return Constant_expression(cvalue.start, value, IntegerT())

    @pe.ExAction
    def createFl(attrs, coords, res_coord):
        value = attrs[0]
        cvalue = coords[0]
        return Constant_expression(cvalue.start, value, FloatT())

    @pe.ExAction
    def createStr(attrs, coords, res_coord):
        value = attrs[0]
        cvalue = coords[0]
        value = value[1:-1].replace("\\n", '\n').replace("\\t", "    ")
        return Constant_expression(cvalue.start, value, StringT(is_const=True, len=len(value)))

    def constant_propagation(self):
        return self

    def Gen(self, symbol_table: ScopeManager, lvalue: bool = True):
        if self.type == StringT():
            if symbol_table.block_type == BlockCategory.Global_block:
                return ir.Constant(self.type.llvm_type(), [ord(char) for char in self.value] + [0])
            else:
                if hasattr(self, "__cached_var"):
                    return self.__cached_var
                else:
                    if hasattr(Constant_expression, "static_cnt"):
                        Constant_expression.static_cnt += 1
                    else:
                        Constant_expression.static_cnt = 1
                    var = ir.GlobalVariable(symbol_table.llvm.module, self.type.llvm_type(), f".str.{Constant_expression.static_cnt}")
                    var.initializer = ir.Constant(self.type.llvm_type(), [ord(char) for char in self.value] + [0])
                    self.__cached_var = var
                    return self.__cached_var
        elif self.type == FloatT():
            return ir.Constant(self.type.llvm_type(), float(self.value))
        else:
            return ir.Constant(self.type.llvm_type(), int(self.value))

    def __str__(self):
        return str(self.value)



@dataclass
class Var:
    pos: pe.Position
    name: Varname
    type: Type

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        varname = attrs[0]
        cvarname = coords[0]
        return Var(cvarname.start, varname, varname.type)

    def relax(self, symbol_table: ScopeManager, lvalue=True):
        lookup_result = symbol_table.synbol_search(self.symbol(), og_check=False)
        name_lookup_result = symbol_table.synbol_search(self.symbol(), type_check=False, og_check=False)
        if not name_lookup_result and not lvalue:
            raise UndefinedVariableError(self.pos, self.name)
        if not lookup_result and not lvalue:
            self.type = name_lookup_result.type
            if isinstance(self.type, ArrayT):
                return Array(self.pos, self.name, self.type, self.type.size).relax(symbol_table)
        return self

    def symbol(self):
        return Symbol(self.name, self.type, False)

    def constant_propagation(self):
        return self


    """ I assume that would be called only from expressions codegen """
    def Gen(self, symbol_table, lvalue: bool = False):
        lookup_result = symbol_table.synbol_search(self.symbol(), og_check=False)
        if lvalue:
            return lookup_result.ll_ref
        else:
            return symbol_table.llvm.builder.load(lookup_result.ll_ref, f"{self.name.mangle_str()}.load")


@dataclass
class Array(Var):
    size: list[Expr]

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        varname, sizes = attrs
        cvarname, cop, cexpr, ccp = coords
        size = sizes
        if isinstance(sizes, int):
            size = [0 for _ in range(sizes)]
        return Array(cvarname.start, varname, ArrayT(varname.type, size), size)

    def relax(self, symbol_table: ScopeManager, lvalue=True):
        if isinstance(self.size[0], int):
            return self
        for idx, expr in enumerate(self.size):
            self.size[idx] = expr.relax(symbol_table, lvalue=False)
            if not isinstance(self.size[idx].type, IntegralT):
                raise ArrayNonIntegerInitializationError(self.pos, self.size[idx].type)
        return self

    def constant_propagation(self):
        for idx, sz in enumerate(self.size):
            if isinstance(sz, Expr):
                self.size[idx] = sz.constant_propagation()
        return self

    """ I assume that would be called only from expressions codegen """

    def Gen(self, symbol_table, lvalue: bool = False):
        lookup_result = symbol_table.synbol_search(self.symbol(), og_check=False)
        if lvalue:
            return lookup_result.ll_ref
        else:
            if self.type.is_function_param:
                return ArrayIndex.get_func_ptr(symbol_table.llvm.builder, lookup_result.ll_ref, [ir.Constant(ir.IntType(32), 0)])
            else:
                return ArrayIndex.get_arr_ptr(symbol_table.llvm.builder, lookup_result.ll_ref, [ir.Constant(ir.IntType(32), 0)])

@dataclass
class Function_prototype :
    pos: pe.Position
    name: Varname
    args: list[Var]
    type: FunctionT

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        name, args = attrs
        cfunc_kw, cvar, cop, cparams, ccp = coords
        return Function_prototype (cvar.start, name, args, FunctionT(name.type, [arg.type for arg in args]))

    @staticmethod
    def construct(varname: Varname, args: list[Var]):
        return Function_prototype (pe.Position(-1,-1,-1), varname, args, FunctionT(varname.type, [arg.type for arg in args]))

    def relax(self, symbol_table: ScopeManager):
        va_cnt = sum(1 if isinstance(arg.type, VarArguT) else 0 for arg in self.args)
        if va_cnt > 1:
            raise MultipleVariadicArgumentsError(self.name.pos)
        names = [self.name]
        for idx, var in enumerate(self.args):
            if var.name in names:
                raise VariableRedefinition(var.pos, var.name, names[names.index(var.name)].pos)
            if isinstance(var, VarArguT) and idx != len(self.args) - 1:
                raise VariadicArgumentNotLastError(var.pos)
            if isinstance(var.type, ArrayT):
                var.type.is_function_param = True
        return self

    def constant_propagation(self):
        return self

    def Gen(self, symbol_table: ScopeManager) -> tuple[FunctionType, list[Symbol]]:
        va_cnt = sum(1 if isinstance(arg.type, VarArguT) else 0 for arg in self.args)
        arguments = []
        symbols = []
        arg_list = self.args[:-1] if va_cnt > 0 else self.args
        for arg in arg_list:
            arguments.append(arg.type.llvm_type())
            symbols.append(Symbol(arg.name, arg.type))
            if isinstance(arg.type, ArrayT):
                for len_idx in range(len(arg.type.size)):
                    arguments.append(ir.IntType(32))
                    symbols.append(Symbol(Varname(pe.Position(), f"{arg.name.name}.len.{len_idx+1}", IntegerT()), IntegerT()))
        return ir.FunctionType(self.type.retT.llvm_type(), arguments), symbols



@dataclass
class Function_declaration:
    pos: pe.Position
    proto: Function_prototype
    external: bool

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        proto = attrs[0]
        cdecl_kw, cproto = coords
        return Function_declaration(cdecl_kw.start, proto, True)

    def relax(self, symbol_table: ScopeManager):
        symbol = self.symbol()
        lookup_result = symbol_table.synbol_search(symbol, local=True, og_check=False)
        if lookup_result and lookup_result.external:
            raise VariableRedefinition(self.pos, self.proto.name, lookup_result.name.pos)
        if not lookup_result:
            symbol_table.add(symbol)
        self.proto = self.proto.relax(symbol_table)
        return self

    def constant_propagation(self):
        self.proto = self.proto.constant_propagation()
        return self

    def symbol(self):
        return Symbol(self.proto.name, self.proto.type, self.external)

    def Gen(self, symbol_table: ScopeManager) -> ir.Function:
        if self.proto.name.name == "Len" and self.proto.name.type == IntegerT():
            return None
        function_proto, symbols = self.proto.Gen(symbol_table)
        func = ir.Function(symbol_table.llvm.module, function_proto, self.proto.name.name)
        for arg_symbol, arg in zip(symbols, func.args):
            arg.name = arg_symbol.name.name
        symbol_table.add(self.symbol().assoc(func))
        return func


@dataclass
class Function_definition:
    pos: pe.Position
    proto: Function_prototype
    body: list[Statement]

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        proto, stmts = attrs
        cfunproto, cbody, cend_kw, cfun_kw = coords
        return Function_definition(cfunproto.start, proto, stmts)

    def relax(self, symbol_table: ScopeManager):
        symbol = self.symbol()
        lookup_result = symbol_table.synbol_search(symbol, local=True, og_check=False)
        if lookup_result:
            if not lookup_result.external:
                raise VariableRedefinition(self.pos, self.proto.name, lookup_result.name.pos)
            else:
                lookup_result.external = False
        else:
            symbol_table.add(symbol)
        self.proto.relax(symbol_table)
        body_symbol_table = symbol_table.new_block(BlockCategory.Function_block)
        func_ret_variable = Var(self.proto.name.pos, self.proto.name, self.proto.type.retT)
        body_symbol_table.add(func_ret_variable.symbol())
        for var in self.proto.args:
            body_symbol_table.add(var.symbol())
        for idx, stmt in enumerate(self.body):
            self.body[idx] = stmt.relax(body_symbol_table)
        return self

    def constant_propagation(self):
        self.proto.constant_propagation()
        for stmt in self.body:
            stmt.constant_propagation()
        return self

    def symbol(self):
        return Symbol(self.proto.name, self.proto.type, False)

    def Gen(self, symbol_table: ScopeManager) -> ir.Function:
        function_proto, symbols = self.proto.Gen(symbol_table)
        func = ir.Function(symbol_table.llvm.module, function_proto, self.proto.name.name)
        symbol_table.add(self.symbol().assoc(func))

        for arg_symbol, arg in zip(symbols, func.args):
            arg.name = arg_symbol.name.name
        entry_block = func.append_basic_block(name="entry")

        return_block = func.append_basic_block(name="return")

        builder = ir.IRBuilder(entry_block)
        body_symbol_table = symbol_table.new_block(BlockCategory.Function_block,
                                                   llvm_entry=LLVMContext(symbol_table.llvm.module, builder, func))

        ret_var = Var(self.proto.name.pos, self.proto.name, self.proto.type.retT)
        ret_val = builder.alloca(ret_var.type.llvm_type(), 1, ret_var.name.name)
        body_symbol_table.add(ret_var.symbol().assoc(ret_val))
        builder.store(ir.Constant(self.proto.type.retT.llvm_type(), self.proto.type.retT.default_value()), ret_val)
        """ 
        Maybe store default value???
        """
        for arg_symbol, arg in zip(symbols, func.args):
            alloc_instr = builder.alloca(arg.type, 1, arg.name)
            body_symbol_table.add(arg_symbol.assoc(alloc_instr))
            builder.store(arg, alloc_instr)

        for stmt in self.body:
            stmt.Gen(body_symbol_table)

        if builder.block.terminator is None:
            builder.branch(return_block)

        return_builder = ir.IRBuilder(return_block)
        return_builder.ret(return_builder.load(ret_val))
        return func



@dataclass
class Subroutine_prototype:
    pos: pe.Position
    name: Varname
    args: list[Var]
    type: FunctionT

    @pe.ExAction
    def create(attrs, coords, res_coord):
        name, args = attrs
        csub_kw, cvar, cop, cparams, ccp = coords
        varname = Varname(cvar.start, name, VoidT())
        return Subroutine_prototype(csub_kw.start, varname, args, FunctionT(VoidT(), [arg.type for arg in args]))

    def relax(self, symbol_table: ScopeManager):
        va_cnt = sum(1 if isinstance(arg.type, VarArguT) else 0 for arg in self.args)
        if va_cnt > 1:
            raise MultipleVariadicArgumentsError(self.name.pos)
        names = [self.name]
        for idx, var in enumerate(self.args):
            if var.name in names:
                raise VariableRedefinition(var.pos, var.name, names[names.index(var.name)].pos)
            if isinstance(var, VarArguT) and idx != len(self.args) - 1:
                raise VariadicArgumentNotLastError(var.pos)
            if isinstance(var.type, ArrayT):
                var.type.is_function_param = True
        return self

    def constant_propagation(self):
        return self

    def Gen(self, symbol_table: ScopeManager) -> tuple[FunctionType, list[Symbol]]:
        va_cnt = sum(1 if isinstance(arg.type, VarArguT) else 0 for arg in self.args)
        arguments = []
        symbols = []
        arg_list = self.args[:-1] if va_cnt > 0 else self.args
        for arg in arg_list:
            arguments.append(arg.type.llvm_type())
            symbols.append(Symbol(arg.name, arg.type))
            if isinstance(arg.type, ArrayT):
                for len_idx in range(len(arg.type.size)):
                    arguments.append(ir.IntType(32))
                    symbols.append(
                        Symbol(Varname(pe.Position(), f"{arg.name.name}.len.{len_idx + 1}", IntegerT()), IntegerT()))
        return ir.FunctionType(self.type.retT.llvm_type(), arguments), symbols

@dataclass
class Subroutine_declaration :
    pos: pe.Position
    proto: Subroutine_prototype
    external: bool

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        proto = attrs[0]
        cdecl_kw, cproto = coords
        return Subroutine_declaration (cdecl_kw.start, proto, True)

    def relax(self, symbol_table: ScopeManager):
        symbol = self.symbol()
        lookup_result = symbol_table.synbol_search(symbol, local=True, og_check=False)
        if lookup_result and lookup_result.external:
            raise VariableRedefinition(self.pos, self.proto.name, lookup_result.name.pos)
        if not lookup_result:
            symbol_table.add(symbol)
        self.proto = self.proto.relax(symbol_table)
        return self

    def constant_propagation(self):
        self.proto.constant_propagation()
        return self

    def symbol(self):
        return Symbol(self.proto.name, self.proto.type, self.external)

    def Gen(self, symbol_table) -> ir.Function:
        subroutine_proto, symbols = self.proto.Gen(symbol_table)
        func = ir.Function(symbol_table.llvm.module, subroutine_proto, self.proto.name.name)
        for arg_symbol, arg in zip(symbols, func.args):
            arg.name = arg_symbol.name.name
        symbol_table.add(self.symbol().assoc(func))
        return func


@dataclass
class Subroutine_definition:
    pos: pe.Position
    proto: Subroutine_prototype
    body: list[Statement]

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        proto, stmts = attrs
        csubproto, cbody, cend_kw, csub_kw = coords
        return Subroutine_definition(csubproto.start, proto, stmts)

    def relax(self, symbol_table: ScopeManager):
        symbol = Symbol(self.proto.name, self.proto.type, False)
        lookup_result = symbol_table.synbol_search(symbol, local=True, og_check=False)
        if lookup_result:
            if not lookup_result.external:
                raise VariableRedefinition(self.pos, self.proto.name, lookup_result.name.pos)
            else:
                lookup_result.external = False
        else:
            symbol_table.add(symbol)
        self.proto.relax(symbol_table)
        body_symbol_table = symbol_table.new_block(BlockCategory.Function_block)
        for var in self.proto.args:
            body_symbol_table.add(var.symbol())
        for idx, stmt in enumerate(self.body):
            self.body[idx] = stmt.relax(body_symbol_table)
        return self

    def constant_propagation(self):
        self.proto.constant_propagation()
        for stmt in self.body:
            stmt.constant_propagation()
        return self

    def symbol(self):
        return Symbol(self.proto.name, self.proto.type, False)

    def Gen(self, symbol_table) -> ir.Function:
        subroutine_proto, symbols = self.proto.Gen(symbol_table)
        sub = ir.Function(symbol_table.llvm.module, subroutine_proto, self.proto.name.name)
        symbol_table.add(self.symbol().assoc(sub))

        for arg_symbol, arg in zip(symbols, sub.args):
            arg.name = arg_symbol.name.name
        entry_block = sub.append_basic_block(name="entry")

        return_block = sub.append_basic_block(name="return")
        return_builder = ir.IRBuilder(return_block)
        return_builder.ret_void()

        builder = ir.IRBuilder(entry_block)
        body_symbol_table = symbol_table.new_block(BlockCategory.Function_block,
                                                   llvm_entry=LLVMContext(symbol_table.llvm.module, builder, sub))

        for arg_symbol, arg in zip(symbols, sub.args):
            alloc_instr = builder.alloca(arg.type, 1, arg.name)
            body_symbol_table.add(arg_symbol.assoc(alloc_instr))
            builder.store(arg, alloc_instr)

        for stmt in self.body:
            stmt.Gen(body_symbol_table)
        if builder.block.terminator is None:
            builder.branch(return_block)
        return sub


@dataclass
class InitializerList:
    pos: pe.Position
    values: list[Union[Expr, list]]
    type: Type

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        vals = attrs[0]
        cop, cvalues, ccp = coords
        return InitializerList(cop.start, vals, VoidT())

    def relax(self, symbol_table: ScopeManager, lvalue: bool = False):
        common_type = None if len(self.values) == 0 else type(self.values[0])
        if not common_type:
            return
        for val in self.values:
            if common_type != type(val):
                raise InvalidInitializerListError(self.pos, common_type, type(val))
        self.size()
        for idx, val in enumerate(self.values):
            self.values[idx] = val.relax(symbol_table, lvalue=False)
        common_type = self.values[0].type
        for val in self.values:
            if common_type != val.type:
                raise InvalidInitializerListError(self.pos, common_type, val.type)
        self.type = common_type
        return self


    def constant_propagation(self):
        for idx, val in enumerate(self.values):
            if isinstance(val, Expr):
                self.values[idx] = val.constant_propagation()
            else:
                val.constant_propagation()
        return self

    def size(self):
        if len(self.values) == 0:
            return 0
        if isinstance(self.values[0], InitializerList):
            common_sz = self.values[0].size()
            for val in self.values:
                val_size = val.size()
                if common_sz != val_size:
                    raise InitializerListDimensionMismatchError(self.pos, common_sz, val_size)
            return [len(self.values)] + common_sz
        else:
            return [len(self.values)]

    def __getitem__(self, item):
        return self.values[item]


@dataclass
class Var_declaration:
    pos: pe.Position
    variable: Var
    init_value: typing.Optional[Union[Expr, InitializerList, None]]

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        var, var_ini = attrs[0], None
        if len(attrs) > 1:
            var_ini = attrs[1]
        cop, cvalues, ccp = coords
        cdim_kw, cvar, cvar_init = coords
        return Var_declaration(cdim_kw.start, var, var_ini)

    def relax(self, symbol_table: ScopeManager):
        lookup_result = symbol_table.synbol_search(self.variable.symbol(), local=True, type_check=False, og_check=False)
        if lookup_result:
            raise VariableRedefinition(self.pos, self.variable.name, lookup_result.name.pos)
        if self.init_value:
            self.init_value = self.init_value.relax(symbol_table)
            if isinstance(self.variable, Array):
                if not self.init_value.type.castable_to(self.variable.type.type):
                    raise TypeConversionError(self.pos, self.init_value.type, self.variable.type.type)
                if isinstance(self.init_value, Expr):
                    raise TypeMismatchDuringInitializationError(self.pos, self.variable.type, self.init_value.type)
                else:
                    self.variable = self.variable.relax(symbol_table)
                    self.variable.size = self.__check_sizes(self.variable.size, self.init_value.size())
                    self.variable.type.size = self.variable.size
                    symbol_table.add(self.variable.symbol())
            else:
                if not self.init_value.type.castable_to(self.variable.type):
                    raise TypeConversionError(self.pos, self.init_value.type, self.variable.type)
                if isinstance(self.init_value, InitializerList):
                    sz = self.init_value.size()
                    self.variable = Array(self.variable.pos, self.variable.name, ArrayT(self.variable.type, sz), sz)
                    symbol_table.add(self.variable.symbol())
                else:
                    if isinstance(self.init_value, Constant_expression) and self.variable.type != self.init_value.type:
                        self.init_value = Constant_expression(self.init_value.pos, self.init_value.value, self.variable.type)
                    symbol_table.add(self.variable.symbol())
        else:
            if isinstance(self.variable, Array):
                if isinstance(self.variable.size[0], int):
                    raise UndefinedLengthInitializationError(self.pos, self.variable.size)
                for idx, sz in enumerate(self.variable.size):
                    if not (isinstance(sz, Constant_expression) and isinstance(sz.type, IntegralT)):
                        raise UndefinedLengthInitializationError(self.pos, self.variable.size)
                    self.variable.size[idx] = self.variable.size[idx].value
            symbol_table.add(self.variable.symbol())
            self.variable = self.variable.relax(symbol_table)
        return self

    def constant_propagation(self):
        self.variable.constant_propagation()
        if self.init_value:
            self.init_value.constant_propagation()
        return self

    def __check_sizes(self, expected_size, given_size):
        if len(expected_size) != len(given_size):
            raise SizeMismatchError(self.pos, expected_size, given_size)
        for sz in expected_size:
            if not isinstance(sz, Constant_expression):
                raise NonConstantSizeError(sz.pos, sz)
            elif sz.value <= 0:
                raise NegativeSizeError(sz.pos, sz)
        result = [sz.value for sz in expected_size]
        for i in range(len(expected_size)):
            if expected_size[i] == 0 and given_size[i] == 0:
                raise UndefinedLengthInitializationError(self.pos, expected_size)
            elif expected_size[i] != 0 and given_size[i] != 0:
                if result[i] != given_size[i]:
                    raise SizeMismatchError(self.pos, expected_size, given_size)
            result[i] = max(result[i], given_size[i])
        return result

    def Gen(self, symbol_table: ScopeManager):
        if symbol_table.block_type != BlockCategory.Global_block:
            alloc_instr = symbol_table.llvm.builder.alloca(self.variable.type.llvm_type(), 1, self.variable.name.mangle_str())
            if self.init_value:
                if isinstance(self.init_value, InitializerList):
                    for idx in itertools.product(*[range(s) for s in self.variable.size]):
                        val = self.init_value.values[idx[0]]
                        for i in range(1, len(idx)):
                            val = val[idx[i]]
                        arr_ptr = ArrayIndex.get_arr_ptr(symbol_table.llvm.builder, alloc_instr, list(idx))
                        relaxed = self.cast_init_value(self.variable.type.type, val, symbol_table, symbol_table.llvm.builder)
                        symbol_table.llvm.builder.store(relaxed, arr_ptr)
                else:
                    buffer = self.cast_init_value(self.variable.type, self.init_value, symbol_table, symbol_table.llvm.builder)
                    symbol_table.llvm.builder.store(buffer, alloc_instr)
            symbol_table.add(self.variable.symbol().assoc(alloc_instr))
            return alloc_instr
        else:
            var = ir.GlobalVariable(symbol_table.llvm.module, self.variable.type.llvm_type(), self.variable.name.mangle_str())
            if self.init_value:
                if isinstance(self.init_value, Constant_expression) and self.variable.type == self.init_value.type:
                    var.initializer = self.cast_init_value(self.variable.type, self.init_value, symbol_table, symbol_table.llvm.builder)
                elif isinstance(self.init_value, (InitializerList, Expr)):
                    sub_proto = ir.FunctionType(ir.VoidType(), [])
                    sub = ir.Function(symbol_table.llvm.module,
                                      sub_proto,
                                      f"__bas_global_var_init.{self.variable.name.mangle_str()}")
                    block = sub.append_basic_block(name="entry")
                    init_builder = ir.IRBuilder(block)
                    symbol_table.llvm.builder = init_builder
                    if isinstance(self.init_value, Expr):
                        var.initializer = ir.Constant(self.init_value.type.llvm_type(), self.init_value.type.default_value())
                        buffer = self.cast_init_value(self.variable.type, self.init_value, symbol_table, symbol_table.llvm.builder)
                        symbol_table.llvm.builder.store(buffer, var)
                    else:
                        var.initializer = ir.Constant(self.variable.type.llvm_type(), self.variable.type.default_value())
                        for idx in itertools.product(*[range(s) for s in self.variable.size]):
                            val = self.init_value.values[idx[0]]
                            for i in range(1, len(idx)):
                                val = val[idx[i]]
                            const_expr_idx = [ir.Constant(ir.IntType(32), idx_idx) for idx_idx in idx]
                            arr_ptr = ArrayIndex.get_arr_ptr(symbol_table.llvm.builder, var, const_expr_idx)
                            relaxed = self.cast_init_value(self.variable.type.type, val, symbol_table, symbol_table.llvm.builder)
                            symbol_table.llvm.builder.store(relaxed, arr_ptr)
                    symbol_table.llvm.builder.ret_void()
                    lookup_result = symbol_table.synbol_search(Program.global_constructor_symbol(), type_check=False, og_check=False)
                    if isinstance(lookup_result.ll_ref, ir.Function):
                        glob_builder = ir.IRBuilder(lookup_result.ll_ref.entry_basic_block)
                        with glob_builder.goto_entry_block():
                            glob_builder.call(sub, [])
                    else:
                        raise RuntimeError("ll_ref isn't ir.Function")
                    symbol_table.llvm.builder = None
            symbol_table.add(self.variable.symbol().assoc(var))
            return var

    def cast_init_value(self, type_a,  val, symbol_table: ScopeManager, builder: ir.IRBuilder):
        value = val.Gen(symbol_table, False)
        if type_a != val.type:
            value = val.type.cast_to(type_a,  builder)(value)
        return value


@dataclass
class Func_or_arr:
    pos: pe.Position
    name: Varname
    args: list[Expr]

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        varname, args = attrs
        cvarname, cop, cargs, ccp = coords
        return Func_or_arr(cvarname.start, varname, args)

    def relax(self, symbol_table: ScopeManager, lvalue=True):
        lookup_result = symbol_table.synbol_search(Symbol(self.name, self.name.type), type_check=False, og_check=False)
        if not lookup_result:
            raise UndefinedVariableError(self.pos, self.name)
        else:
            if isinstance(lookup_result.type, ArrayT):
                result = ArrayIndex(self.pos, self.name, self.args, self.name.type)
                return result.relax(symbol_table)
            elif isinstance(lookup_result.type, FunctionT):
                result = Function_call(self.pos, self.name, self.args, self.name.type)
                return result.relax(symbol_table)
        return self

    def constant_propagation(self):
        for idx, arg in enumerate(self.args):
            self.args[idx] = arg.constant_propagation()
        return self


@dataclass
class Function_call:
    pos: pe.Position
    name: Varname
    args: list[Expr]
    type: Type

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        func_name, args = attrs
        cfunc, cop, cargs, ccp = coords
        if isinstance(func_name, str):
            func_name = Varname(cfunc.start, func_name, VoidT())
        return Function_call(cfunc.start, func_name, args, func_name.type)

    @staticmethod
    @pe.ExAction
    def create_print(attrs, coords, res_coord):
        args = attrs[0]
        cprint, cargs = coords
        func_name = Varname(cprint.start, "Print", VoidT())
        return Function_call(cprint.start, func_name, args, func_name.type)

    def relax(self, symbol_table: ScopeManager, lvalue=True):
        for idx, arg in enumerate(self.args):
            self.args[idx] = arg.relax(symbol_table, False)
        if self.name.name == "Print":
            for arg in self.args:
                if not isinstance(arg.type, (NumericT, StringT)):
                    raise UndefinedFunctionError(self.pos, self.name, FunctionT(VoidT(), [arg.type]))
        else:
            lookup_result = symbol_table.synbol_search(self.symbol(), og_check=False, accumulate=True)
            name_lookup_result = symbol_table.synbol_search(self.symbol(), type_check=False, og_check=False, accumulate=True)
            if name_lookup_result is None:
                raise UndefinedVariableError(self.pos, self.name)
            func_subst = None
            for symb in name_lookup_result:
                if self.symbol().type.castable_to(symb.type):
                    func_subst = symb
                    break
            if not lookup_result and not func_subst:
                raise UndefinedFunctionError(self.pos, self.name, self.symbol().type)
        return self

    def constant_propagation(self):
        for idx, arg in enumerate(self.args):
            self.args[idx] = arg.constant_propagation()
        return self

    def symbol(self):
        return Symbol(self.name, FunctionT(self.name.type, [arg.type for arg in self.args]))

    def print_symbols(self):
        return [Symbol(self.name, FunctionT(self.name.type, [arg.type])) for arg in self.args]

    def Gen(self, symbol_table: ScopeManager, lvalue: bool = True):
        const_zero = ir.Constant(ir.IntType(32), 0)
        const_one = ir.Constant(ir.IntType(32), 1)
        if self.name.name == "Print":
            for arg in self.args:
                lookup_result = symbol_table.synbol_search(Program.print_symbol(arg.type))
                value = arg.Gen(symbol_table, False)
                if isinstance(value, ir.GlobalVariable) and isinstance(arg.type, StringT):
                    value = ArrayIndex.get_arr_ptr(symbol_table.llvm.builder, value, [const_zero])
                symbol_table.llvm.builder.call(lookup_result.ll_ref, [value])
        elif self.name.name == "Len" and self.name.type == IntegerT():
            arg = self.args[0].symbol()
            len_val = None
            if isinstance(self.args[0], Array):
                len_val = symbol_table.synbol_search(Symbol(Varname(pe.Position(), f"{arg.name.name}.len.1", IntegerT()), IntegerT()))
            elif isinstance(self.args[0], ArrayIndex):
                lookup_result = symbol_table.synbol_search(arg)
                idx = len(lookup_result.type.size) - len(arg.type.size) + 1
                len_val = symbol_table.synbol_search(Symbol(Varname(pe.Position(), f"{arg.name.name}.len.{idx}", IntegerT()), IntegerT()))
            return symbol_table.llvm.builder.load(len_val.ll_ref)
        else:
            lookup_result = symbol_table.synbol_search(self.symbol(), og_check=False, accumulate=True)
            name_lookup_result = symbol_table.synbol_search(self.symbol(), type_check=False, og_check=False, accumulate=True)
            func = None
            args = []
            if lookup_result:
                func = lookup_result[0].ll_ref
                for arg in self.args:
                    arg_value = arg.Gen(symbol_table, False)
                    if isinstance(arg.type, StringT) and isinstance(arg_value, ir.GlobalVariable):
                        arg_value = ArrayIndex.get_arr_ptr(symbol_table.llvm.builder, arg_value, [const_zero])
                    args.append(arg_value)
                    if isinstance(arg, Array):
                        if arg.type.is_function_param:
                            arg_symbol = arg.symbol()
                            len_val = None
                            if isinstance(arg, Array):
                                len_val = symbol_table.synbol_search(Symbol(Varname(pe.Position(), f"{arg_symbol.name.name}.len.1", IntegerT()), IntegerT()))
                            elif isinstance(arg, ArrayIndex):
                                lookup_result = symbol_table.synbol_search(arg_symbol)
                                idx = len(lookup_result.type.size) - len(arg_symbol.type.size) + 1
                                len_val = symbol_table.synbol_search(Symbol(Varname(pe.Position(), f"{arg_symbol.name.name}.len.{idx}", IntegerT()),IntegerT()))
                            args.append(symbol_table.llvm.builder.load(len_val.ll_ref))
                        else:
                            for sz in arg.size:
                                args.append(ir.Constant(ir.IntType(32), sz))
            else:
                """ Casting types somehow """
                found_symb = None
                for symb in name_lookup_result:
                    if self.symbol().type.castable_to(symb.type):
                        found_symb = symb
                        func = symb.ll_ref
                        break
                for call_arg_type, func_arg_type, call_arg in zip(self.symbol().type.argsT, found_symb.type.argsT, self.args):
                    arg = call_arg.Gen(symbol_table, False)
                    if call_arg_type != func_arg_type:
                        arg = call_arg_type.cast_to(func_arg_type, symbol_table.llvm.builder)(arg)
                    if isinstance(call_arg.type, StringT) and isinstance(arg, ir.GlobalVariable):
                        arg = ArrayIndex.get_arr_ptr(symbol_table.llvm.builder, arg, [const_zero])
                    args.append(arg)
                    if isinstance(call_arg, Array):
                        if call_arg.type.is_function_param:
                            arg_symbol = call_arg.symbol()
                            len_val = None
                            if isinstance(call_arg, Array):
                                len_val = symbol_table.synbol_search(Symbol(Varname(pe.Position(), f"{arg_symbol.name.name}.len.1", IntegerT()), IntegerT()))
                            elif isinstance(call_arg, ArrayIndex):
                                lookup_result = symbol_table.synbol_search(arg_symbol)
                                idx = len(lookup_result.type.size) - len(arg_symbol.type.size) + 1
                                len_val = symbol_table.synbol_search(Symbol(Varname(pe.Position(), f"{arg_symbol.name.name}.len.{idx}", IntegerT()),IntegerT()))
                            args.append(symbol_table.llvm.builder.load(len_val.ll_ref))
                        else:
                            for sz in call_arg.size:
                                args.append(ir.Constant(ir.IntType(32), sz))
            if isinstance(func, ir.Function):
                name = "call"
                if func.ftype.return_type == ir.VoidType():
                    name = ""
                return symbol_table.llvm.builder.call(func, args, name)


@dataclass
class ArrayIndex:
    pos: pe.Position
    name: Varname
    args: list[Expr]
    type: Type

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        pass

    def relax(self, symbol_table: ScopeManager):
        for idx, arg in enumerate(self.args):
            self.args[idx] = arg.relax(symbol_table)
            if not isinstance(self.args[idx].type, IntegralT):
                raise ArrayNonIntegerIndexError(self.pos, self.args[idx].type)
        lookup_result = symbol_table.synbol_search(Symbol(self.name, self.name.type), type_check=False, og_check=False)
        if not lookup_result:
            raise UndefinedVariableError(self.pos, self.name)
        if len(self.args) != len(lookup_result.type.size):
            if len(self.args) > len(lookup_result.type.size):
                raise ArrayDimensionMismatchError(self.pos, len(lookup_result.type.size), len(self.args))
            else:
                self.type = ArrayT(self.name.type,
                                   lookup_result.type.size[len(self.args):len(lookup_result.type.size)],
                                   lookup_result.type.is_function_param)
        return self

    def constant_propagation(self):
        for idx, arg in enumerate(self.args):
            self.args[idx] = arg.constant_propagation()
        return self

    def symbol(self):
        return Symbol(self.name, self.name.type)

    def Gen(self, symbol_table: ScopeManager, lvalue: bool = True):
        lookup_result = symbol_table.synbol_search(Symbol(self.name, self.name.type), type_check=False, og_check=False)
        if isinstance(lookup_result.ll_ref, (ir.AllocaInstr, ir.GlobalVariable)):
            const_zero = ir.Constant(ir.IntType(32), 0)
            const_one = ir.Constant(ir.IntType(32), 1)
            indices = []
            for arg in self.args:
                idx = arg.Gen(symbol_table, False)
                idx = arg.type.sub(symbol_table.llvm.builder, "idx_sub")(idx, const_one)
                indices.append(idx)
            gep_idx = None
            if lookup_result.type.is_function_param:
                gep_idx = ArrayIndex.get_func_ptr(symbol_table.llvm.builder, lookup_result.ll_ref, indices)
            else:
                gep_idx = ArrayIndex.get_arr_ptr(symbol_table.llvm.builder, lookup_result.ll_ref, indices)
            if lvalue:
                return gep_idx
            else:
                return symbol_table.llvm.builder.load(gep_idx, "gep_idx_load")

    @staticmethod
    def get_func_ptr(builder: ir.IRBuilder, arr_alloca: ir.AllocaInstr, indices: list):
        gep_idx = arr_alloca
        for idx in indices:
            gep_load = builder.load(gep_idx, "gep_load")
            gep_idx = builder.gep(gep_load, [idx], True, "gep_idx")
        return gep_idx

    @staticmethod
    def get_arr_ptr(builder: ir.IRBuilder, arr_alloca: Union[ir.AllocaInstr, ir.GlobalVariable], indices: list):
        const_zero = ir.Constant(ir.IntType(32), 0)
        gep_idx = arr_alloca
        for idx in indices:
            gep_idx = builder.gep(gep_idx, [const_zero, idx], True, "gep_idx")
        return gep_idx


@dataclass
class ExitStatement(Statement):
    pos: pe.Position

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        pass


@dataclass
class ExitFor(ExitStatement):
    name: Union[Var, None]

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        var = None
        if len(attrs) != 0:
            varname = attrs[0]
            var = Var(varname.pos, varname, varname.type)
        cexit = coords[0]
        return ExitFor(cexit.start, var)

    def relax(self, symbol_table: ScopeManager):
        lookup_result = symbol_table.block_search(BlockCategory.For_block, accumulate=True)
        if not lookup_result:
            raise InappropriateExitError(self.pos, self)
        if self.name:
            name_lookup_result = symbol_table.synbol_search(self.name.symbol(), og_check=False)
            if not name_lookup_result:
                raise UndefinedVariableError(self.pos, self.name)
            for blocks in lookup_result:
                if blocks.block_obj.name == self.name.name:
                    return self
        return self

    def Gen(self, symbol_table: ScopeManager):
        lookup_result = symbol_table.block_search(BlockCategory.For_block, accumulate=True)
        block = None
        for blocks in lookup_result:
            if blocks.block_obj.name == self.name.name:
                block = blocks
                break
        symbol_table.llvm.builder.branch(block.llvm.obj)


@dataclass
class ExitWhile(ExitStatement):

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        cexit, cdo = coords
        return ExitWhile(cexit.start)

    def relax(self, symbol_table: ScopeManager):
        lookup_result = symbol_table.block_search(BlockCategory.Loop_block )
        if not lookup_result:
            raise InappropriateExitError(self.pos, self)
        return self

    def Gen(self, symbol_table: ScopeManager):
        lookup_result = symbol_table.block_search(BlockCategory.Loop_block )
        lookup_result.llvm.builder.branch(lookup_result.llvm.obj)



@dataclass
class ExitSubroutine(ExitStatement):

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        cexit, csub = coords
        return ExitSubroutine(cexit.start)

    def relax(self, symbol_table: ScopeManager):
        lookup_result = symbol_table.block_search(BlockCategory.Sub_block)
        if not lookup_result:
            raise InappropriateExitError(self.pos, self)
        return self

    def Gen(self, symbol_table: ScopeManager):
        lookup_result = symbol_table.block_search(BlockCategory.Sub_block)
        if isinstance(lookup_result.llvm.obj, ir.Function):
            lookup_result.llvm.builder.branch(lookup_result.llvm.obj.basic_blocks[-1])


@dataclass
class ExitFunction(ExitStatement):

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        cexit, cfunc = coords
        return ExitFunction(cexit.start)

    def relax(self, symbol_table: ScopeManager):
        lookup_result = symbol_table.block_search(BlockCategory.Function_block)
        if not lookup_result:
            raise InappropriateExitError(self.pos, self)
        return self

    def Gen(self, symbol_table: ScopeManager):
        lookup_result = symbol_table.block_search(BlockCategory.Function_block)
        if isinstance(lookup_result.llvm.obj, ir.Function):
            lookup_result.llvm.builder.branch(lookup_result.llvm.obj.basic_blocks[-1])



@dataclass
class Assignment_state(Statement):
    pos: pe.Position
    variable: Union[Var, Func_or_arr]
    expr: Expr

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        var, expr = attrs
        if isinstance(var, Varname):
            var = Var(var.pos, var, var.type)
        cvar, ceq, cexpr = coords
        return Assignment_state(cvar.start, var, expr)

    def relax(self, symbol_table: ScopeManager):
        self.variable = self.variable.relax(symbol_table)
        global_lookup_result = symbol_table.synbol_search(self.variable.symbol(), type_check=False, og_check=False)
        local_lookup_result = symbol_table.synbol_search(self.variable.symbol(), local=True, type_check=False, og_check=False)
        if local_lookup_result:
            pass
        else:
            if global_lookup_result:
                pass
            else:
                if isinstance(self.variable, Var):
                    result = Var_declaration(self.pos, self.variable, self.expr)
                    return result.relax(symbol_table)
                if not isinstance(self.variable, ArrayIndex):
                    raise UndefinedVariableError(self.pos, self.variable.name)
        self.expr = self.expr.relax(symbol_table, lvalue=False)
        if not self.expr.type.castable_to(self.variable.type):
            raise TypeConversionError(self.pos, self.expr.type, self.variable.type)
        return self

    def constant_propagation(self):
        if isinstance(self.variable, Func_or_arr):
            self.variable = self.variable.constant_propagation()
        self.expr = self.expr.constant_propagation()
        return self

    def Gen(self, symbol_table: ScopeManager):
        const_zero = ir.Constant(ir.IntType(32), 0)
        variable = self.variable.Gen(symbol_table, True)
        expr_val = self.expr.Gen(symbol_table, False)
        if isinstance(variable, (ir.AllocaInstr, ir.GlobalVariable, ir.GEPInstr)):
            if isinstance(expr_val, ir.GlobalVariable) and isinstance(self.expr.type, StringT):
                expr_val = ArrayIndex.get_arr_ptr(symbol_table.llvm.builder, expr_val, [const_zero])
            if self.variable.type != self.expr.type:
                expr_val = self.expr.type.cast_to(self.variable.type, symbol_table.llvm.builder)(expr_val)
            if isinstance(self.variable.type, StringT) and isinstance(self.expr.type, StringT):
                if not self.expr.type.is_const:
                    str_copy_symbol = Program.string_copy_symbol()
                    lookup_result = symbol_table.synbol_search(str_copy_symbol, type_check=False)
                    if isinstance(symbol_table.llvm.builder, ir.IRBuilder):
                        expr_val = symbol_table.llvm.builder.call(lookup_result.ll_ref, [expr_val],"str_copy_val")
            symbol_table.llvm.builder.store(expr_val, variable)


@dataclass
class For_loop(Statement):
    variable: Var
    cond_coord: pe.Position
    start: Expr
    start_coord: pe.Fragment
    end: Expr
    end_coord: pe.Fragment
    body: list[Statement]
    next: Var
    next_coord: pe.Fragment

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        varname, start, end, body, next_varname = attrs
        cfor_kw, cvar, cass, cstart, cto_kw, cend, cstmts, ckw_next, cnext_varname = coords
        var = Var(varname.pos, varname, varname.type)
        next_variable = Var(next_varname.pos, next_varname, next_varname.type)
        return For_loop(var, cvar.start, start, cstart, end, cend, body, next_variable, cnext_varname)

    def relax(self, symbol_table: ScopeManager):
        lookup_result = symbol_table.synbol_search(self.variable.symbol(), local=True, type_check=False, og_check=False)
        if lookup_result:
            raise VariableRedefinition(self.cond_coord, self.variable.name, lookup_result.name)
        if not isinstance(self.variable.type, IntegralT):
            raise NonIntegerForLoopError(self.cond_coord, self.variable.type)
        symbol_table.add(self.variable.symbol())
        if self.variable.name != self.next.name:
            raise ForLoopCounterMismatchError(self.next_coord, self.variable.name, self.next.name)
        self.start = self.start.relax(symbol_table, lvalue=True)
        self.end = self.end.relax(symbol_table, lvalue=True)
        if not self.start.type.castable_to(self.variable.type):
            raise TypeConversionError(self.start_coord, self.start.type, self.variable.type)
        if not self.end.type.castable_to(self.variable.type):
            raise TypeConversionError(self.start_coord, self.end.type, self.variable.type)
        for_block = symbol_table.new_block(BlockCategory.For_block, block_obj=self.variable)
        for idx, stmt in enumerate(self.body):
            self.body[idx] = stmt.relax(for_block)
        return self

    def constant_propagation(self):
        self.start = self.start.constant_propagation()
        self.end = self.end.constant_propagation()
        for stmt in self.body:
            stmt.constant_propagation()
        return self

    def Gen(self, symbol_table: ScopeManager):
        start = self.Gen_start(symbol_table)
        end = self.Gen_end(symbol_table)
        if isinstance(symbol_table.llvm.builder, ir.IRBuilder):
            if isinstance(symbol_table.llvm.builder.function, ir.Function):
                builder = symbol_table.llvm.builder
                func = builder.function
                idx_alloca = builder.alloca(self.variable.type.llvm_type(), 1)
                builder.store(start, idx_alloca)
                symbol_table.add(self.variable.symbol().assoc(idx_alloca))
                idx = func.basic_blocks.index(symbol_table.llvm.builder.block) + 1
                cond_block = func.insert_basic_block(idx,
                                                name=suffix_check(builder.block.name, ".for.cond"))
                cond_block_builder = ir.IRBuilder(cond_block)
                body_block = func.insert_basic_block(idx + 1,
                                                name=suffix_check(builder.block.name, ".for.body"))
                body_block_builder = ir.IRBuilder(body_block)
                inc_block = func.insert_basic_block(idx + 2,
                                               name=suffix_check(builder.block.name, ".for.inc"))
                inc_block_builder = ir.IRBuilder(inc_block)
                end_block = func.insert_basic_block(idx + 3,
                                               name=suffix_check(builder.block.name, ".for.end"))
                for_table = symbol_table.new_block(BlockCategory.For_block,
                                                   block_obj=self.variable,
                                                   llvm_entry=LLVMContext(symbol_table.llvm.module,
                                                                                   body_block_builder,
                                                                                   end_block))
                builder.branch(cond_block)
                self.Gen_condition (cond_block_builder, idx_alloca, end, body_block, end_block)
                self.Gen_increment(inc_block_builder, idx_alloca, cond_block)

                for stmt in self.body:
                    stmt.Gen(for_table)

                if body_block_builder.block.terminator is None:
                    body_block_builder.branch(inc_block)

                builder.position_at_end(end_block)

    def Gen_start(self, symbol_table: ScopeManager):
        start = self.start.Gen(symbol_table)
        if self.start.type != self.variable.type:
            start = self.start.type.cast_to(self.variable.type, symbol_table.llvm.builder)(start)
        return start

    def Gen_end(self, symbol_table: ScopeManager):
        end = self.end.Gen(symbol_table)
        if self.end.type != self.variable.type:
            end = self.end.type.cast_to(self.variable.type, symbol_table.llvm.builder)(end)
        return end

    def Gen_condition (self, builder: ir.IRBuilder, idx_alloca, end_value, body_block, end_block):
        for_idx = builder.load(idx_alloca, "for.idx")
        for_cond = builder.icmp_signed("<=", for_idx, end_value)
        builder.cbranch(for_cond, body_block, end_block)

    def Gen_increment(self, builder: ir.IRBuilder, idx_alloca, block):
        inc_idx = builder.load(idx_alloca, "for.idx")
        inc_add = builder.add(inc_idx, ir.Constant(self.variable.type.llvm_type(), 1))
        builder.store(inc_add, idx_alloca)
        builder.branch(block)


@dataclass
class While_loop(Statement):
    pos: pe.Position
    condition: Union[Expr, None]
    body: list[Statement]
    type: WhileT

    def __init__(self, body, condition, type_):
        self.body = body
        self.condition = condition
        self.type = type_

    def relax(self, symbol_table: ScopeManager):
        if self.condition:
            self.condition = self.condition.relax(symbol_table, lvalue=False)
            if not isinstance(self.condition.type, IntegralT):
                raise WhileConditionTypeError(self.pos, self.condition.type)
        while_block = symbol_table.new_block(BlockCategory.Loop_block )
        for idx, stmt in enumerate(self.body):
            self.body[idx] = stmt.relax(while_block)
        return self

    def constant_propagation(self):
        if self.condition:
            self.condition = self.condition.constant_propagation()
        for stmt in self.body:
            stmt.constant_propagation()
        return self

    def Gen(self, symbol_table: ScopeManager):
        if isinstance(symbol_table.llvm.builder, ir.IRBuilder):
            if isinstance(symbol_table.llvm.builder.function, ir.Function):
                builder = symbol_table.llvm.builder
                func = builder.function
                idx = func.basic_blocks.index(symbol_table.llvm.builder.block) + 1

                cond_block = func.insert_basic_block(idx,
                                                name=suffix_check(builder.block.name, ".for.cond"))
                cond_block_builder = ir.IRBuilder(cond_block)
                body_block = func.insert_basic_block(idx + 1,
                                                name=suffix_check(builder.block.name, ".for.body"))
                body_block_builder = ir.IRBuilder(body_block)
                end_block = func.insert_basic_block(idx + 2,
                                               name=suffix_check(builder.block.name, ".for.end"))
                while_table = symbol_table.new_block(BlockCategory.Loop_block ,
                                                     llvm_entry=LLVMContext(symbol_table.llvm.module,
                                                                                     body_block_builder,
                                                                                     end_block))
                if self.type == WhileT.PreWhile or self.type == WhileT.PreUntil:
                    builder.branch(cond_block)
                else:
                    builder.branch(body_block)
                self.Gen_condition (symbol_table, cond_block_builder, body_block, end_block)

                for stmt in self.body:
                    stmt.Gen(while_table)

                if body_block_builder.block.terminator is None:
                    body_block_builder.branch(cond_block)

                builder.position_at_end(end_block)

    def Gen_condition (self, symbol_table: ScopeManager, builder: ir.IRBuilder, body_block, end_block):
        if self.condition:
            buffer = symbol_table.llvm.builder
            symbol_table.llvm.builder = builder
            cond_val = self.condition.Gen(symbol_table)
            symbol_table.llvm.builder = buffer
            const_val = ir.Constant(self.condition.type.llvm_type(), 0)
            op = "!=" if self.type == WhileT.PreWhile or self.type.PostWhile else "=="
            while_cond = self.condition.type.cmp(op, builder, "while.cond")(cond_val, const_val)
            builder.cbranch(while_cond, body_block, end_block)
        else:
            builder.branch(body_block)

    def __repr__(self):
        return f"While(type={self.type})"


@dataclass
class IfElse_Clause(Statement):
    pos: pe.Position
    condition: Expr
    then_branch: list[Statement]
    else_branch: list[Statement]

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        cond, then_branch, else_branch = attrs
        cif, ccond, cthen_kw, cthen_br, celse_stmt, cend_kw, cif_kw = coords
        return IfElse_Clause(ccond.start, cond, then_branch, else_branch)

    def relax(self, symbol_table: ScopeManager):
        self.condition = self.condition.relax(symbol_table)
        if not isinstance(self.condition.type, IntegralT):
            raise IfConditionTypeError(self. pos, self.condition.type)
        if_block = symbol_table.new_block(BlockCategory.IfThenBlock)
        for idx, stmt in enumerate(self.then_branch):
            self.then_branch[idx] = stmt.relax(if_block)
        else_block = symbol_table.new_block(BlockCategory.If_block)
        for idx, stmt in enumerate(self.else_branch):
            self.else_branch[idx] = stmt.relax(else_block)
        return self

    def constant_propagation(self):
        self.condition = self.condition.constant_propagation()
        return self

    def Gen(self, symbol_table: ScopeManager):
        if len(self.else_branch) == 0:
            self.codegen_if_then(symbol_table)
        else:
            self.codegen_if_else(symbol_table)

    def codegen_if_else(self, symbol_table: ScopeManager):
        cond_val = self.condition.Gen(symbol_table)
        if isinstance(symbol_table.llvm.builder, ir.IRBuilder):
            if isinstance(symbol_table.llvm.builder.function, ir.Function):
                builder = symbol_table.llvm.builder
                func = builder.function
                idx = func.basic_blocks.index(symbol_table.llvm.builder.block) + 1

                if_then_block = func.insert_basic_block(idx,
                                                name=suffix_check(builder.block.name, ".if.then"))
                if_then_block_builder = ir.IRBuilder(if_then_block)
                if_else_block = func.insert_basic_block(idx + 1,
                                                name=suffix_check(builder.block.name, ".if.else"))
                if_else_block_builder = ir.IRBuilder(if_else_block)
                end_block = func.insert_basic_block(idx + 2,
                                               name=suffix_check(builder.block.name, ".if.end"))
                if_then_table = symbol_table.new_block(BlockCategory.IfThenBlock,
                                                       llvm_entry=LLVMContext(symbol_table.llvm.module,
                                                                                       if_then_block_builder,
                                                                                       end_block))
                if_else_table = symbol_table.new_block(BlockCategory.If_block,
                                                       llvm_entry=LLVMContext(symbol_table.llvm.module,
                                                                                       if_else_block_builder,
                                                                                       end_block))
                const_val = ir.Constant(self.condition.type.llvm_type(), 0)
                if_cond = self.condition.type.cmp("!=", builder, "if.cond")(cond_val, const_val)
                builder.cbranch(if_cond, if_then_block, if_else_block)

                for stmt in self.then_branch:
                    stmt.Gen(if_then_table)
                if if_then_block_builder.block.terminator is None:
                    if_then_block_builder.branch(end_block)

                for stmt in self.else_branch:
                    stmt.Gen(if_else_table)
                if if_else_block_builder.block.terminator is None:
                    if_else_block_builder.branch(end_block)

                builder.position_at_end(end_block)

    def codegen_if_then(self, symbol_table: ScopeManager):
        cond_val = self.condition.Gen(symbol_table)
        if isinstance(symbol_table.llvm.builder, ir.IRBuilder):
            if isinstance(symbol_table.llvm.builder.function, ir.Function):
                builder = symbol_table.llvm.builder
                func = builder.function
                idx = func.basic_blocks.index(symbol_table.llvm.builder.block) + 1
                if_then_block = func.insert_basic_block(idx,
                                                   name=suffix_check(builder.block.name, ".if.then"))
                if_then_block_builder = ir.IRBuilder(if_then_block)
                end_block = func.insert_basic_block(idx + 1,
                                               name=suffix_check(builder.block.name, ".if.end"))
                if_then_table = symbol_table.new_block(BlockCategory.IfThenBlock,
                                                       llvm_entry=LLVMContext(symbol_table.llvm.module,
                                                                                       if_then_block_builder,
                                                                                       end_block))

                const_val = ir.Constant(self.condition.type.llvm_type(), 0)
                if_cond = self.condition.type.cmp("!=", builder, "if.cond")(cond_val, const_val)
                builder.cbranch(if_cond, if_then_block, end_block)

                for stmt in self.then_branch:
                    stmt.Gen(if_then_table)
                if if_then_block_builder.block.terminator is None:
                    if_then_block_builder.branch(end_block)

                builder.position_at_end(end_block)


@dataclass
class UnaryOpExpr(Expr):
    pos: pe.Position
    op: str
    unary_expr: Expr

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        op, left = attrs
        cop, cleft = coords
        return UnaryOpExpr(cop.start, op, left)

    def relax(self, symbol_table: ScopeManager, lvalue=True):
        self.unary_expr = self.unary_expr.relax(symbol_table, lvalue)
        if isinstance(self.unary_expr.type, StringT) or (not isinstance(self.unary_expr.type, NumericT)):
            raise UnaryTypeMismatchError(self.pos, self.unary_expr.type, self.op)
        self.type = self.unary_expr.type
        return self

    def constant_propagation(self):
        self.unary_expr = self.unary_expr.constant_propagation()
        if isinstance(self.unary_expr, Constant_expression):
            if self.unary_expr.type != StringT():
                if isinstance(self.unary_expr.type, IntegralT):
                    return Constant_expression(self.pos, int(f"{self.op}{self.unary_expr.value}"), self.unary_expr.type)
                elif isinstance(self.unary_expr.type, FloatingPointT):
                    return Constant_expression(self.pos, float(f"{self.op}{self.unary_expr.value}"), self.unary_expr.type)
        return self

    def Gen(self, symbol_table: ScopeManager, lvalue: bool = True):
        expr_val = self.unary_expr.Gen(symbol_table, False)
        if self.op == '-':
            if isinstance(self.unary_expr.type, NumericT):
                expr_val = self.unary_expr.type.neg(symbol_table.llvm.builder, "expr.val.neg")(expr_val)
        return expr_val



@dataclass
class BinOpExpr(Expr):
    pos: pe.Position
    left: Expr
    op: str
    right: Expr

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        left, op, right = attrs
        cleft, cop, cright = coords
        return BinOpExpr(cleft.start, left, op, right)

    def relax(self, symbol_table: ScopeManager, lvalue=True):
        self.left = self.left.relax(symbol_table, lvalue)
        self.right = self.right.relax(symbol_table, lvalue)
        if isinstance(self.left.type, NumericT) and isinstance(self.right.type, NumericT):
            result_type = None
            if self.op in ('+', '-', '*'):
                if self.left.type.castable_to(self.right.type):
                    result_type = self.right.type
                elif self.right.type.castable_to(self.left.type):
                    result_type = self.left.type
            elif self.op == '/':
                result_type = DoubleT()
            elif self.op in ('>', '<', '>=', '<=', '=', '<>'):
                result_type = BoolT()
            else:
                raise UndefinedBinaryOperatorError(self.pos, self.left.type, self.op, self.right.type)
            if not result_type:
                raise BinaryTypeMismatchError(self.pos, self.left.type, self.op, self.right.type)
            self.type = result_type
        elif isinstance(self.left.type, StringT) and isinstance(self.right.type, StringT):
            if self.op != '+':
                raise BinaryTypeMismatchError(self.pos, self.left.type, self.op, self.right.type)
            self.type = StringT()
        else:
            raise BinaryTypeMismatchError(self.pos, self.left.type, self.op, self.right.type)
        return self

    def constant_propagation(self):
        self.left = self.left.constant_propagation()
        self.right = self.right.constant_propagation()
        if isinstance(self.left, Constant_expression) and isinstance(self.right, Constant_expression):
            if self.left.type == StringT() and self.right.type == StringT() and self.op == '+':
                return Constant_expression(self.pos, f"{self.left.value}{self.right.value}", StringT())
            elif isinstance(self.left.type, NumericT) and isinstance(self.right.type, NumericT):
                if self.op in ('>', '<', '>=', '<=', '=', '<>'):
                    self.op = "!=" if self.op == "<>" else self.op
                    self.op = "==" if self.op == "=" else self.op
                    return Constant_expression(self.pos,
                                     1 if eval(f"{self.left.value}{self.op}{self.right.value}") else 0,
                                     BoolT())
                elif self.op in ('+', '-', '*', '/'):
                    return Constant_expression(self.pos,
                                     eval(f"{self.left.value}{self.op}{self.right.value}"),
                                     self.left.type if self.left.type.priority > self.right.type.priority else self.right.type)
        return self

    def Gen(self, symbol_table: ScopeManager, lvalue: bool = True):
        lhs_val = self.left.Gen(symbol_table, False)
        rhs_val = self.right.Gen(symbol_table, False)
        result_val = None
        if self.type == StringT():
            str_concat_symbol = Program.string_concat_symbol()
            lookup_result = symbol_table.synbol_search(str_concat_symbol, type_check=False)
            if isinstance(symbol_table.llvm.builder, ir.IRBuilder):
                result_val = symbol_table.llvm.builder.call(lookup_result.ll_ref, [lhs_val, rhs_val], "str_concat_val")
        elif isinstance(self.left.type, NumericT) and isinstance(self.right.type, NumericT):
            if self.op in ('>', '<', '>=', '<=', '=', '<>'):
                result_val = self.type.cmp(self.op, symbol_table.llvm.builder, "bin_cmp_val")(lhs_val, rhs_val)
            else:
                if self.left.type != self.type:
                    lhs_val = self.left.type.cast_to(self.type, symbol_table.llvm.builder)(lhs_val)
                if self.right.type != self.type:
                    rhs_val = self.right.type.cast_to(self.type, symbol_table.llvm.builder)(rhs_val)
                if self.op == "+":
                    result_val = self.type.add(symbol_table.llvm.builder, "bin_add_val")(lhs_val, rhs_val)
                elif self.op == "-":
                    result_val = self.type.sub(symbol_table.llvm.builder, "bin_sub_val")(lhs_val, rhs_val)
                elif self.op == "*":
                    result_val = self.type.mul(symbol_table.llvm.builder, "bin_mul_val")(lhs_val, rhs_val)
                elif self.op == "/":
                    result_val = self.type.div(symbol_table.llvm.builder, "bin_div_val")(lhs_val, rhs_val)
        return result_val


@dataclass
class Program:
    decls: list[Union[Subroutine_declaration , Function_declaration, Subroutine_definition, Function_definition, Var_declaration]]
    symbol_table: ScopeManager

    @staticmethod
    @pe.ExAction
    def create(attrs, coords, res_coord):
        global_decls = attrs[0]
        declarations = Program.standart_library() + global_decls
        program = Program(declarations, ScopeManager(block_type=BlockCategory.Global_block))
        program = program.constant_propagation()
        program = program.relax()
        return program

    def relax(self):
        for idx, decl in enumerate(self.decls):
            self.decls[idx] = decl.relax(self.symbol_table)
        return self

    def constant_propagation(self):
        for idx, decl in enumerate(self.decls):
            self.decls[idx] = decl.constant_propagation()
        return self

    def Gen(self, module_name=None):
        program_module = ir.Module(name=module_name if module_name else __file__)
        program_module.triple = binding.get_default_triple()
        program_module.data_layout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
        # global_constr = GlobalCtorArray(program_module, "variable_decl_constructor")
        global_constr_sub = ir.Function(program_module, ir.FunctionType(ir.VoidType(), []), "variable_decl_constructor")
        global_builder = ir.IRBuilder(global_constr_sub.append_basic_block("entry"))
        global_builder.ret_void()
        global_constr_symbol = Program.global_constructor_symbol().assoc(global_constr_sub)
        self.symbol_table = ScopeManager(block_type=BlockCategory.Global_block,
                                        llvm_entry=LLVMContext(program_module))
        self.symbol_table.add(global_constr_symbol)

        for decl in self.decls:
            decl.Gen(self.symbol_table)
        return program_module

    @staticmethod
    def standart_library() -> list:
        standart_decls = []
        types = [IntegerT(), LongT(), FloatT(), DoubleT(), StringT()]

        for tp in types:
            symbol = Program.print_symbol(tp)
            print_arg = [Var(pe.Position(), Varname(pe.Position(), "val", tp), tp)]
            print_proto = Subroutine_prototype(pe.Position(), symbol.name, print_arg, symbol.type)
            print_sub = Subroutine_declaration (pe.Position(), print_proto, True)
            standart_decls.append(print_sub)

        default_pos = pe.Position(-1, -1, -1)
        len_arg = [Var(default_pos, Varname(default_pos, "arr", Type()), ArrayT(Type(), [], True))]
        len_proto = Function_prototype (default_pos, Varname(default_pos, "Len", IntegerT()), len_arg,
                                  FunctionT(IntegerT(), [arg.type for arg in len_arg]))
        len_func = Function_declaration(default_pos, len_proto, True)
        standart_decls.append(len_func)

        default_pos = pe.Position(-1, -1, -1)
        str_concat_arg = [Var(default_pos, Varname(default_pos, "lhs", StringT()), StringT()),
                          Var(default_pos, Varname(default_pos, "rhs", StringT()), StringT())]
        str_concat_proto = Function_prototype (default_pos, Varname(default_pos, "StringConcat", StringT()), str_concat_arg,
                                  FunctionT(StringT(), [arg.type for arg in str_concat_arg]))
        str_concat_func = Function_declaration(default_pos, str_concat_proto, True)
        standart_decls.append(str_concat_func)

        str_copy_arg = [Var(default_pos, Varname(default_pos, "lhs", StringT()), StringT())]
        str_copy_proto = Function_prototype (default_pos, Varname(default_pos, "StringCopy", StringT()), str_copy_arg,
                                         FunctionT(StringT(), [arg.type for arg in str_copy_arg]))
        str_copy_func = Function_declaration(default_pos, str_copy_proto, True)
        standart_decls.append(str_copy_func)

        return standart_decls

    @staticmethod
    def print_symbol(type_a: Type):
        if isinstance(type_a,  NumericT) or isinstance(type_a,  StringT):
            print_varname = Varname(pe.Position(), f"Print{type_a.mangle_suff}", VoidT())
            return Symbol(print_varname, FunctionT(VoidT(), [type_a]), True)
        else:
            raise RuntimeError("Bad print type")

    @staticmethod
    def len_symbol():
        len_arg_type = ArrayT(Type(), [], True)
        len_varname = Varname(pe.Position(), "Len", IntegerT())
        return Symbol(len_varname, FunctionT(VoidT(), [len_arg_type]), True)

    @staticmethod
    def global_constructor_symbol():
        return Symbol(Varname(None, "variable_decl_constructor", VoidT()), FunctionT(VoidT(), []))

    @staticmethod
    def string_concat_symbol():
        return Symbol(Varname(pe.Position(), "StringConcat", StringT()), FunctionT(StringT(), [StringT(), StringT()]), True)

    @staticmethod
    def string_copy_symbol():
        return Symbol(Varname(pe.Position(), "StringCopy", StringT()), FunctionT(StringT(), [StringT()]), True)