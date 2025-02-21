from pathlib import Path
import re
from ast_t.my_ast import *
from ast_t import parser_edsl as pe
import sys

# parser
def make_keyword(image):
    return pe.Terminal(image, image, lambda name: None, re_flags=re.IGNORECASE, priority=10)

IDENTIFIER = pe.Terminal('IDENTIFIER', '[A-Za-z][A-Za-z0-9_]*', str)
INTEGER = pe.Terminal('INTEGER', '[0-9]+', int)
STRING = pe.Terminal('STRING', '\"[^\"]*\"', str)
FLOAT = pe.Terminal('FLOAT', '[0-9]+\\.([0-9]*)?(e[-+]?[0-9]+)?', float)


KW_SUB, KW_FUNCTION, KW_END, KW_DIM = map(make_keyword, 'sub function end dim'.split())
KW_EXIT, KW_DECLARE, KW_PRINT = map(make_keyword, "exit declare print".split())
KW_IF, KW_THEN, KW_ELSE, KW_UNTIL, KW_WHILE, KW_DO, KW_FOR, KW_TO, KW_NEXT, KW_LOOP = \
    map(make_keyword, 'if then else until while do for to next loop'.split())

NProgram, NGlobal_declaration, NDeclaration, NSubroutine_prototype, NFunction_prototype , NSubroutine_definition, NFunction_definition = \
    map(pe.NonTerminal, "Program Global_declaration Declaration Subroutine_prototype Function_prototype  Subroutine_definition Function_definition".split())

NSubroutine_declaration, NFunction_declaration , NVar_declaration, NVar_initialization, NInitialValueList, NInitializer_list = \
    map(pe.NonTerminal, "Subroutine_declaration Function_declaration  Var_declaration Var_initialization InitialValueList Initializer_list".split())

NInitializerListValue, NPara_list, NVarnameOrArrayParam, NComma_list, NVarname_or_array_argument = \
    map(pe.NonTerminal, "InitializerListValue Para_list VarnameOrArrayParam Comma_list Varname_or_array_argument".split())

NArg_list , NFunc_or_arr, NFunction_call, NVarname, NType, NStatements, NStatement, NAssignment_state = \
    map(pe.NonTerminal, "Arg_list  Func_or_arr Function_call Varname Type Statements Statement Assignment_state".split())

NNon_empty_arg, NNon_empty_para, NNemp_statement = \
    map(pe.NonTerminal, "Non_empty_arg Non_empty_para Nemp_statement".split())

NExit_statement, NElse_Clause , NLoop, NFor_loop , NWhile_loop, NPredefined_or_post = \
    map(pe.NonTerminal, "Exit_statement Else_Clause  Loop For_loop  While_loop Predefined_or_post".split())

NPredefined, NPost, NPost_expression = \
    map(pe.NonTerminal, "Predefined Post Post_expression ".split())

NExpression, NCmpOp, NArithmetic_expression, NAdd_operator, NTerm, NTer, NConstant, NMulOp = \
    map(pe.NonTerminal, 'Expression CmpOp Arithmetic_expression Add_operator Term Ter Constant MulOp'.split())

NProgram |= NGlobal_declaration, Program.create

NGlobal_declaration |= NDeclaration, NGlobal_declaration, lambda vd, vds: [vd] + vds
NGlobal_declaration |= lambda: []
NDeclaration |= NSubroutine_declaration
NDeclaration |= NSubroutine_definition
NDeclaration |= NFunction_declaration
NDeclaration |= NFunction_definition
NDeclaration |= NVar_declaration

NSubroutine_prototype |= KW_SUB, IDENTIFIER, "(", NPara_list, ")", Subroutine_prototype.create
NFunction_prototype |= KW_FUNCTION, NVarname, "(", NPara_list, ")", Function_prototype .create
NSubroutine_definition |= NSubroutine_prototype, NStatements, KW_END, KW_SUB, Subroutine_definition.create
NFunction_definition |= NFunction_prototype , NStatements, KW_END, KW_FUNCTION, Function_definition.create
NSubroutine_declaration |= KW_DECLARE, NSubroutine_prototype, Subroutine_declaration.create
NFunction_declaration |= KW_DECLARE, NFunction_prototype , Function_declaration .create
NVar_declaration |= KW_DIM, NVarname_or_array_argument, NVar_initialization, Var_declaration.create

NVar_initialization |= '=', NExpression
NVar_initialization |= '=', NInitialValueList
NVar_initialization |= lambda: None
NInitialValueList |= '{', NInitializer_list, '}', InitializerList.create
NInitialValueList |= '{}', InitializerList.create
NInitializer_list |= NInitializerListValue, ',', NInitializer_list, lambda v, vs: [v] + vs
NInitializer_list |= NInitializerListValue, lambda v: [v]
NInitializerListValue |= NExpression
NInitializerListValue |= NInitialValueList

NPara_list |= NVarnameOrArrayParam, ",", NNon_empty_para, lambda vd, vds: [vd] + vds
NPara_list |= NVarnameOrArrayParam, lambda vd: [vd]
NPara_list |= lambda: []

NNon_empty_para |= NVarnameOrArrayParam, ",", NNon_empty_para, lambda vd, vds: [vd] + vds
NNon_empty_para |= NVarnameOrArrayParam, lambda vd: [vd]

NComma_list |= ',', NComma_list, lambda vs: 1 + vs
NComma_list |= lambda: 1

NVarnameOrArrayParam |= NVarname, Var.create
NVarnameOrArrayParam |= NVarname, "(", NComma_list, ")", Array.create

NArg_list |= NExpression, ",", NNon_empty_arg, lambda vd, vds: [vd] + vds
NArg_list |= NExpression, lambda vd: [vd]
NArg_list |= lambda: []

NNon_empty_arg |= NExpression, ",", NNon_empty_arg, lambda vd, vds: [vd] + vds
NNon_empty_arg |= NExpression, lambda vd: [vd]

NVarname_or_array_argument |= NVarname, Var.create
NVarname_or_array_argument |= NVarname, "(", NNon_empty_arg, ")", Array.create
NVarname_or_array_argument |= NVarname, "(", NComma_list, ")", Array.create

NFunc_or_arr |= NVarname, "(", NArg_list , ")", Func_or_arr.create
NFunc_or_arr |= IDENTIFIER, "(", NArg_list , ")", Function_call.create

NFunction_call |= KW_PRINT, NNon_empty_arg, Function_call.create_print

NVarname |= IDENTIFIER, NType, Varname.create
NType |= "%", lambda: IntegerT()
NType |= "&", lambda: LongT()
NType |= "!", lambda: FloatT()
NType |= "#", lambda: DoubleT()
NType |= '$', lambda: StringT()

NStatements |= NStatement, NNemp_statement, lambda vd, vds: [vd] + vds
NStatements |= NExit_statement, lambda vd: [vd]
NStatements |= NStatement, lambda vd: [vd]
NStatements |= lambda: []

NNemp_statement |= NStatement, NNemp_statement, lambda vd, vds: [vd] + vds
NNemp_statement |= NExit_statement, lambda vd: [vd]
NNemp_statement |= NStatement, lambda vd: [vd]

NStatement |= NVar_declaration
NStatement |= NAssignment_state
NStatement |= NFunc_or_arr, "=", NExpression, Assignment_state.create
NStatement |= NFunc_or_arr
NStatement |= NFunction_call
NStatement |= NLoop
NStatement |= KW_IF, NExpression, KW_THEN, NStatements, NElse_Clause , KW_END, KW_IF, IfElse_Clause.create

NAssignment_state |= NVarname, "=", NExpression, Assignment_state.create
NExit_statement |= KW_EXIT, KW_FOR, ExitFor.create
NExit_statement |= KW_EXIT, KW_FOR, NVarname, ExitFor.create
NExit_statement |= KW_EXIT, KW_DO, ExitWhile.create
NExit_statement |= KW_EXIT, KW_LOOP, ExitWhile.create
NExit_statement |= KW_EXIT, KW_SUB, ExitSubroutine.create
NExit_statement |= KW_EXIT, KW_FUNCTION, ExitFunction.create

NElse_Clause |= KW_ELSE, NStatements
NElse_Clause |= lambda: []

NLoop |= NFor_loop
NLoop |= NWhile_loop

NFor_loop  |= KW_FOR, NVarname, "=", NExpression, KW_TO, NExpression, NStatements, KW_NEXT, NVarname, For_loop.create

NWhile_loop |= KW_DO, NPredefined_or_post

NPredefined |= NExpression, NStatements, KW_LOOP, lambda expression, stmts: (expression, stmts)
NPost |= NStatements, KW_LOOP, NPost_expression, lambda stmts, type_and_expr: While_loop(stmts, type_and_expr[1], type_and_expr[0])

NPredefined_or_post |= KW_WHILE, NPredefined, lambda x: While_loop(x[1], x[0], WhileT.PreWhile)
NPredefined_or_post |= KW_UNTIL, NPredefined, lambda x: While_loop(x[1], x[0], WhileT.PreUntil)
NPredefined_or_post |= NPost

NPost_expression |= KW_WHILE, NExpression, lambda expr: (WhileT.PostWhile, expr)

NPost_expression |= KW_UNTIL, NExpression, lambda expr: (WhileT.PostUntil, expr)

NPost_expression |= lambda: (WhileT.Endless, None)

NExpression |= NArithmetic_expression
NExpression |= NArithmetic_expression, NCmpOp, NArithmetic_expression, BinOpExpr.create


def op_builder(x):
    def op():
        return x
    return op

for op in ('>', '<', '>=', '<=', '=', '<>'):
    NCmpOp |= op, op_builder(op)

NArithmetic_expression |= NTerm
NArithmetic_expression |= NAdd_operator, NTerm, UnaryOpExpr.create
NArithmetic_expression |= NArithmetic_expression, NAdd_operator, NTerm, BinOpExpr.create

NAdd_operator |= '+', lambda: '+'
NAdd_operator |= '-', lambda: '-'

NTerm |= NTer
NTerm |= NTerm, NMulOp, NTer, BinOpExpr.create

NMulOp |= '*', lambda: '*'
NMulOp |= '/', lambda: '/'

NTer |= NVarname, Var.create
NTer |= NConstant
NTer |= '(', NExpression, ')'
NTer |= NFunc_or_arr

NConstant |= INTEGER, Constant_expression.createInt
NConstant |= FLOAT, Constant_expression.createFl
NConstant |= STRING, Constant_expression.createStr

p = pe.Parser(NProgram)
p.add_skipped_domain('\\s')
p.add_skipped_domain('\\\'.*?\\n')

for filename in sys.argv[1:]:
    try:
        with open(filename, encoding='utf-8') as f:
            tree = p.parse(f.read())
            module = tree.Gen()
            with open(Path(filename).with_suffix('').with_suffix('.ll'), "w+") as fout:
                fout.write(str(module))
    except pe.Error as e:
        print(f'Error {e.pos}: {e.message}')
