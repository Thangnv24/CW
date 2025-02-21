from llvmlite import ir

##############################################################################
# Lớp kiểu con trỏ mờ (Opaque Pointer) trong LLVM
# Class for LLVM Opaque Pointer Type
##############################################################################
class OpaquePtrType(ir.PointerType):
    """Biểu diễn kiểu con trỏ mờ (không xác định kiểu dữ liệu trỏ tới) trong LLVM
    Represents LLVM opaque pointer type (pointer without specified pointee type)"""

    def __init__(self, pointee=ir.VoidType(), addrspace=0):
        self.is_opaque = isinstance(pointee, ir.VoidType)
        self.pointee = pointee
        self.addrspace = addrspace

    def _to_string(self):
        if self.is_opaque:
            return "ptr"
        elif self.addrspace != 0:
            return "{0} addrspace({1})*".format(self.pointee, self.addrspace)
        else:
            return "{0}*".format(self.pointee)

    def __str__(self):
        return "ptr"

    def __eq__(self, other):
        if isinstance(other, ir.PointerType):
            return (self.pointee, self.addrspace) == (other.pointee,
                                                      other.addrspace)
        else:
            return False

    def __hash__(self):
        return hash(ir.PointerType)

    def gep(self, i):
        """Xử lý kiểu dữ liệu khi thực hiện getelementptr
        Resolve pointee type for getelementptr operations"""
        if not isinstance(i.type, ir.IntType):
            raise TypeError(i.type)
        return self.pointee

    @property
    def intrinsic_name(self):
        return 'p%d%s' % (self.addrspace, self.pointee.intrinsic_name)


##############################################################################
# Lớp xây dựng hàm khởi tạo toàn cục
# Global Constructor Array Class
##############################################################################
class GlobalCtorArray(ir.GlobalValue):
    """Quản lý mảng hàm khởi tạo toàn cục dạng LLVM
    Manages LLVM global constructor array"""

    def __init__(self, module, constructor_name=None, addrspace=0):
        self.value_type = ir.ArrayType(ir.LiteralStructType([
            ir.IntType(32),
            OpaquePtrType(),
            OpaquePtrType()
        ]), 1)

        super(GlobalCtorArray, self).__init__(
            module,
            self.value_type.as_pointer(addrspace),
            name="llvm.global_ctors"
        )

        self.initializer = None
        if constructor_name:
            self.set_constructor_function_name(constructor_name)
        self.unnamed_addr = False
        self.addrspace = addrspace
        self.align = None
        self.parent.add_global(self)

    def descr(self, buf):
        """Mô tả cấu trúc dữ liệu cho LLVM IR
        Generate LLVM IR description"""
        kind = "appending global"
        buf.append("{kind} {type}".format(kind=kind, type=self.value_type))
        if self.initializer.type != self.value_type:
            raise TypeError("got initializer of type %s "
                            "for global value type %s"
                            % (self.initializer.type, self.value_type))
        buf.append(" " + self.initializer.get_reference())
        buf.append("\n")

    def set_constructor_function_name(self, name: str):
        """Thiết lập hàm khởi tạo
        Set constructor function name"""
        const_val = ir.Constant(self.value_type, [[
            ir.Constant(ir.IntType(32), 65535),
            ir.Constant(OpaquePtrType(), f"@{name}"),
            ir.Constant(OpaquePtrType(), "null")
        ]])
        self.initializer = const_val


##############################################################################
# Hàm hỗ trợ định dạng nhãn
# Label formatting helper function
##############################################################################
def suffix_check(label, suffix):
    if len(label) > 100:
        count = 50
        return ''.join([label[:count], '..', suffix])
    else:
        return label + suffix


##############################################################################
# Lớp lệnh GetElementPointer cho con trỏ mờ
# Opaque Pointer GEP Instruction Class
##############################################################################
class OpaqueGEPInstr(ir.Instruction):
    """Xử lý lệnh getelementptr cho con trỏ mờ
    Handles getelementptr instructions for opaque pointers"""

    def __init__(self, parent, ptr, indices, inbounds, name):
        typ = OpaquePtrType()
        super(OpaqueGEPInstr, self).__init__(
            parent, typ, "getelementptr",
            [ptr] + list(indices), name=name
        )
        self.pointer = ptr
        self.indices = indices
        self.inbounds = inbounds

    def descr(self, buf):
        """Mô tả lệnh trong LLVM IR
        Generate instruction description for LLVM IR"""
        indices = ['{0} {1}'.format(i.type, i.get_reference())
                   for i in self.indices]
        op = "getelementptr inbounds" if self.inbounds else "getelementptr"
        buf.append(f"{op} {self.pointer.type.pointee}, "
                   f"{self.pointer.type} {self.pointer.get_reference()}, "
                   f"{', '.join(indices)}"
                   f"{self._stringify_metadata(leading_comma=True)}\n")


##############################################################################
# Hàm tạo lệnh GEP cho con trỏ mờ
# Opaque Pointer GEP Instruction Creator
##############################################################################
def create_opaque_gep(self, ptr, indices, inbounds=False, name=''):
    """Tạo lệnh getelementptr cho con trỏ mờ
    Create getelementptr instruction for opaque pointers"""
    instr = OpaqueGEPInstr(
        self.block,
        ptr,
        indices,
        inbounds=inbounds,
        name=name
    )
    self._insert(instr)
    return instr

