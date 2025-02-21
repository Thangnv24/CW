
from typing import Union
from .error import *
from enum import Enum

################################################################################
# Loại khối trong bảng ký hiệu
# Symbol table block category
################################################################################
class BlockCategory(Enum):
    Undefined = 0
    Global_block = 1
    Function_block = 2
    Sub_block = 3
    If_block = 4
    Loop_block = 5
    For_block = 6
    IfThenBlock = 7 # for enum class


################################################################################
# Thông tin ký hiệu trong bảng
# Symbol entry representation
################################################################################
class Symbol:
    def __init__(self, name, type_a, external=False, assoc_obj: object = None):
        self.name = name
        self.type = type_a
        self.external = external
        self.ll_ref = assoc_obj

    def assoc(self, assoc_obj: object):
    # def bind_llvm_reference(self, llvm_ref: object):
        """Liên kết đối tượng LLVM với ký hiệu
        Bind LLVM object to symbol"""

        self.ll_ref = assoc_obj
        # self.llvm_ref = llvm_ref
        return self


################################################################################
# Ngữ cảnh LLVM cho khối
# LLVM execution context
################################################################################
class LLVMContext:
    def __init__(self, module, builder=None, assoc_obj=None):
        self.module = module
        self.builder = builder
        self.obj = assoc_obj

    def builder(self, builder):
        if builder:
            self.builder = builder
        return self

    def assoc(self, assoc_obj):
        if assoc_obj:
            self.obj = assoc_obj
        return self

################################################################################
# Quản lý phạm vi ký hiệu
# Symbol scope manager
################################################################################
class ScopeManager:

    def __init__(self, parent=None,
                 block_type: BlockCategory = BlockCategory.Undefined,
                 block_obj: object = None,
                 llvm_entry: LLVMContext = None):
        self.parent = parent
        self.table = []
        self.children = []
        self.block_type = block_type
        self.block_obj = block_obj
        self.llvm = llvm_entry

    """Thêm ký hiệu mới vào phạm vi
        Add new symbol to current scope"""
    def add(self, symbol: Symbol):
        check = self.synbol_search(symbol, local=True)
        if check:
            raise VariableRedefinition(symbol.name.pos, symbol.name, check.name.pos)
        self.table.append(symbol)

    """Tìm kiếm ký hiệu trong phạm vi
        Search for symbol in scope hierarchy"""
    def synbol_search(self, symbol: Symbol, local=False, name_check=True, type_check=True, og_check=True, accumulate=False) \
            -> Union[list[Symbol], Symbol, None]:
        current = self
        list_look = []
        while current:
            for cu in current.table:
                check_look = True
                if name_check:
                    check_look &= symbol.name == cu.name
                if type_check:
                    check_look &= symbol.type == cu.type
                if og_check:
                    check_look &= symbol.external == cu.external
                if check_look:
                    if accumulate:
                        list_look += [cu]
                    else:
                        return cu
            if local:
                if accumulate:
                    return None if len(list_look) == 0 else list_look
                else:
                    return None
            current = current.parent
        if accumulate:
            return None if len(list_look) == 0 else list_look
        else:
            return None

    """Tìm kiếm phạm vi theo loại
        Find scope by category"""
    # Search symbol table with specific block type
    def block_search(self, block_type: BlockCategory, accumulate: bool = False):
        current = self
        list_look = []
        while current:
            if current.block_type == block_type:
                if accumulate:
                    list_look += [current]
                else:
                    return current
            current = current.parent
        if accumulate:
            return None if len(list_look) == 0 else list_look
        else:
            return None

    """Tạo phạm vi con mới
        Create new nested scope"""
    def new_block(self,
                  block_type: BlockCategory = BlockCategory.Undefined,
                  block_obj: object = None,
                  llvm_entry: LLVMContext = None):

        self.children.append(ScopeManager(self, block_type=block_type, block_obj=block_obj, llvm_entry=llvm_entry))
        return ScopeManager(self, block_type=block_type, block_obj=block_obj, llvm_entry=llvm_entry)

    """Thiết lập trình xây dựng IR
        Configure IR builder for scope"""
    def builder(self, builder):
        self.llvm.builder(builder)
        return self

    """Liên kết thực thể với phạm vi
        Associate entity with scope"""
    def assoc(self, assoc_obj: object):
        self.llvm.assoc(assoc_obj)
        return self


