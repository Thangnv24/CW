; ModuleID = "D:\downloads\bmstu\7st_sem\main\main_cw\src\my_ast.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

@"llvm.global_ctors" = appending global [1 x {i32, ptr, ptr}] [{i32, ptr, ptr} {i32 65535, ptr @variable_decl_constructor, ptr null}]
define void @"variable_decl_constructor"()
{
entry:
  ret void
}

declare void @"PrintI"(i32 %"val")

declare void @"PrintL"(i64 %"val")

declare void @"PrintF"(float %"val")

declare void @"PrintD"(double %"val")

declare void @"PrintS"(i32* %"val")

declare i32* @"StringConcat"(i32* %"lhs", i32* %"rhs")

declare i32* @"StringCopy"(i32* %"lhs")

define i32* @"Join"(i32** %"items", i32 %"items.len.1")
{
entry:
  %"Join" = alloca i32*, i32 1
  store i32* null, i32** %"Join"
  %"items.1" = alloca i32**, i32 1
  store i32** %"items", i32*** %"items.1"
  %"items.len.1.1" = alloca i32, i32 1
  store i32 %"items.len.1", i32* %"items.len.1.1"
  %"cS" = alloca i32*, i32 1
  %"idx_sub" = sub i32 1, 1
  %"gep_load" = load i32**, i32*** %"items.1"
  %"gep_idx" = getelementptr inbounds i32*, i32** %"gep_load", i32 %"idx_sub"
  %"gep_idx_load" = load i32*, i32** %"gep_idx"
  %"idx_sub.1" = sub i32 2, 1
  %"gep_load.1" = load i32**, i32*** %"items.1"
  %"gep_idx.1" = getelementptr inbounds i32*, i32** %"gep_load.1", i32 %"idx_sub.1"
  %"gep_idx_load.1" = load i32*, i32** %"gep_idx.1"
  %"str_concat_val" = call i32* @"StringConcat"(i32* %"gep_idx_load", i32* %"gep_idx_load.1")
  store i32* %"str_concat_val", i32** %"cS"
  %"cS.load" = load i32*, i32** %"cS"
  call void @"PrintS"(i32* %"cS.load")
  br label %"return"
return:
  %".10" = load i32*, i32** %"Join"
  ret i32* %".10"
}
