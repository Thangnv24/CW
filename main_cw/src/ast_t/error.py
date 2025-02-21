from .import parser_edsl  as pe

# Lớp cơ sở cho các lỗi ngữ nghĩa (semantic errors)
# Base class for semantic errors
class SemanticError(pe.Error):
    pass


### Lỗi liên quan đến khai báo và sử dụng biến ###
### Errors related to variable declaration and usage ###

# Biến được định nghĩa lại sau khi đã được khai báo
# Variable is redefined after being declared
class VariableRedefinition(SemanticError):
    def __init__(self, pos, name, prev_def):
        self.pos = pos
        self.name = name
        self.prev_def = prev_def

    @property
    def message(self):
        return f'Redeclaring a symbol {self.name}, previously announced at {self.prev_def}'


# Biến được sử dụng nhưng chưa được khai báo
# Variable is used but not declared
class UndefinedVariableError(SemanticError):
    def __init__(self, pos, name):
        self.pos = pos
        self.name = name

    @property
    def message(self):
        return f'Symbol {self.name} not defined'


### Lỗi liên quan đến toán tử ###
### Errors related to operators ###

# Lỗi không tương thích kiểu dữ liệu với toán tử nhị phân
# Incompatible types for binary operator
class BinaryTypeMismatchError(SemanticError):
    def __init__(self, pos, left, op, right):
        self.pos = pos
        self.left = left
        self.op = op
        self.right = right

    @property
    def message(self):
        return f'Incompatible types: {self.left} {self.op} {self.right}'


# Toán tử nhị phân không xác định hoặc chưa được định nghĩa
# Undefined or unsupported binary operator
class UndefinedBinaryOperatorError(SemanticError):
    def __init__(self, pos, left, op, right):
        self.pos = pos
        self.left = left
        self.op = op
        self.right = right

    @property
    def message(self):
        return f'Undefined operation: {self.left} {self.op} {self.right}'


# Phép toán một ngôi không xác định
# Undefined or unsupported unary operator
class UnaryTypeMismatchError(SemanticError):
    def __init__(self, pos, expr_type, op):
        self.pos = pos
        self.expr_type = expr_type
        self.op = op

    @property
    def message(self):
        return f'Undefined unary operation: {self.op} {self.expr_type}'


### Lỗi liên quan đến mảng ###
### Errors related to arrays ###

# Mảng được truy cập bằng chỉ số không phải kiểu nguyên
# Array is indexed by a non-integer type
class ArrayNonIntegerIndexError(SemanticError):
    def __init__(self, pos, type_):
        self.pos = pos
        self.type = type_

    @property
    def message(self):
        return f'The array is indexed by a non-integer type: {self.type}'


# Số chiều của mảng không khớp với danh sách chỉ số
# Array dimension does not match the indexing list
class ArrayDimensionMismatchError(SemanticError):
    def __init__(self, pos, expected_len, found_len):
        self.pos = pos
        self.expected_len = expected_len
        self.found_len = found_len

    @property
    def message(self):
        return f'The array dimension is less than the indexing list: {self.expected_len} < {self.found_len}'


### Lỗi liên quan đến điều kiện ###
### Errors related to conditions ###

# Điều kiện trong câu lệnh if không phải kiểu nguyên
# Condition in if statement is not of integer type
class IfConditionTypeError(SemanticError):
    def __init__(self, pos, type_):
        self.pos = pos
        self.type = type_

    @property
    def message(self):
        return f'The condition has type {self.type} instead of integer'


# Điều kiện trong câu lệnh while không phải kiểu nguyên
# Condition in while loop is not of integer type
class WhileConditionTypeError(SemanticError):
    def __init__(self, pos, type_):
        self.pos = pos
        self.type = type_

    @property
    def message(self):
        return f'The loop has type {self.type} instead of integer'


### Lỗi liên quan đến khởi tạo ###
### Errors related to initialization ###

# Khởi tạo mảng với kiểu dữ liệu không phải nguyên
# Array initialization with non-integer type
class ArrayNonIntegerInitializationError(SemanticError):
    def __init__(self, pos, type_):
        self.pos = pos
        self.type = type_

    @property
    def message(self):
        return f'The whole type was expected, received {self.type}'


# Khởi tạo danh sách với kích thước không phải hằng số
# List initialization with non-constant size
class NonConstantSizeError(SemanticError):
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    @property
    def message(self):
        return f'The size is not constant when initializing a list: {self.size}'


# Khởi tạo danh sách với kích thước âm
# List initialization with negative size
class NegativeSizeError(SemanticError):
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    @property
    def message(self):
        return f'The size cannot be negative: {self.size}'


### Lỗi liên quan đến hàm ###
### Errors related to functions ###

# Hàm không được định nghĩa
# Function is not defined
class UndefinedFunctionError(SemanticError):
    def __init__(self, pos, name, type):
        self.pos = pos
        self.name = name
        self.type = type

    @property
    def message(self):
        return f'Function {self.name}: {self.type} not defined'


# Lỗi thoát không phù hợp
# Inappropriate exit statement
class InappropriateExitError(SemanticError):
    def __init__(self, pos, exit_stmt):
        self.pos = pos
        self.exit_stmt = exit_stmt

    @property
    def message(self):
        return f'Uncertain exit: {self.exit_stmt}'

### Lỗi liên quan đến tham số hàm ###
### Errors related to function parameters ###

# Khai báo nhiều hơn 1 đối số biến trong hàm
# Declaring more than one variadic argument in function
class MultipleVariadicArgumentsError(SemanticError):
    def __init__(self, pos):
        self.pos = pos

    @property
    def message(self):
        return f'More than 1 variable argument declaration in functions:{self.pos}'


# Khai báo đối số biến không phải là cuối cùng
# Variadic argument is not declared last
class VariadicArgumentNotLastError(SemanticError):
    def __init__(self, pos):
        self.pos = pos

    @property
    def message(self):
        return f"The declaration of a variable argument is not the last one:{self.pos}"


### Lỗi khởi tạo nâng cao ###
### Advanced initialization errors ###

# Danh sách khởi tạo không phù hợp
# Inappropriate initializer list
class InvalidInitializerListError(SemanticError):
    def __init__(self, pos, common_type, bad_type):
        self.pos = pos
        self.common_type = common_type
        self.bad_type = bad_type

    @property
    def message(self):
        return f'Initialization list not defined: expected: {self.common_type}, met: {self.bad_type}'


# Lỗi chiều khởi tạo không khớp
# Initializer list dimension mismatch
class InitializerListDimensionMismatchError(SemanticError):
    def __init__(self, pos, common_dims, found_dims):
        self.pos = pos
        self.common_dims = common_dims
        self.found_dims = found_dims

    @property
    def message(self):
        return f'Initialization list dimensions mismatch: expected: {self.common_dims}, met: {self.found_dims}'


### Lỗi chuyển đổi kiểu ###
### Type conversion errors ###

# Lỗi chuyển đổi kiểu không hợp lệ
# Invalid type conversion
class TypeConversionError(SemanticError):
    def __init__(self, pos, from_type, to_type):
        self.pos = pos
        self.from_type = from_type
        self.to_type = to_type

    @property
    def message(self):
        return f'Unable to convert type:{self.from_type} to type:{self.to_type}'


### Lỗi khởi tạo chi tiết ###
### Detailed initialization errors ###

# Lỗi kiểu dữ liệu khi khởi tạo
# Type mismatch during initialization
class TypeMismatchDuringInitializationError(SemanticError):
    def __init__(self, pos, var_type, expr_type):
        self.pos = pos
        self.var_type = var_type
        self.expr_type = expr_type

    @property
    def message(self):
        return f'Type mismatch: {self.var_type} vs {self.expr_type} during initialization'


# Lỗi kích thước không xác định khi khởi tạo
# Undefined size during initialization
class UndefinedLengthInitializationError(SemanticError):
    def __init__(self, pos, undefined_length):
        self.pos = pos
        self.undefined_length = undefined_length

    @property
    def message(self):
        return f'Undefined size during initialization:{self.undefined_length}'


### Lỗi vòng lặp For ###
### For loop errors ###

# Kiểu dữ liệu không phải số nguyên trong vòng For
# Non-integer type in For loop
class NonIntegerForLoopError(SemanticError):
    def __init__(self, pos, type_):
        self.pos = pos
        self.type = type_

    @property
    def message(self):
        return f'Expected integer type in For loop, received: {self.type}'


# Bộ đếm vòng lặp không khớp
# Loop counter mismatch
class ForLoopCounterMismatchError(SemanticError):
    def __init__(self, pos, true_index, false_index):
        self.pos = pos
        self.true_index = true_index
        self.false_index = false_index

    @property
    def message(self):
        return f'Counter mismatch: expected {self.true_index}, got {self.false_index}'

### Lỗi khởi tạo chi tiết ###
### Detailed initialization errors ###

# Lỗi độ dài khởi tạo không khớp
# Initialization length mismatch
class SizeMismatchError(SemanticError):
    def __init__(self, pos, expect, given):
        self.pos = pos
        self.expect = '[' + ','.join([str(length) for length in expect]) + ']'
        self.given = given

    @property
    def message(self):
        return f'Size mismatch during initialization: expected {self.expect}, received {self.given}'

