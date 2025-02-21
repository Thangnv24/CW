; ModuleID = "D:\downloads\bmstu\7st_sem\main\main_cw\src\my_ast.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

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

define i32* @"thang"(i32* %"thang_a", i32** %"thang_b", i32 %"thang_b.len.1")
{
entry:
  %"thang" = alloca i32*, i32 1
  store i32* null, i32** %"thang"
  %"thang_a.1" = alloca i32*, i32 1
  store i32* %"thang_a", i32** %"thang_a.1"
  %"thang_b.1" = alloca i32**, i32 1
  store i32** %"thang_b", i32*** %"thang_b.1"
  %"thang_b.len.1.1" = alloca i32, i32 1
  store i32 %"thang_b.len.1", i32* %"thang_b.len.1.1"
  %"iI" = alloca i32, i32 1
  store i32 0, i32* %"iI"
  %".10" = load i32, i32* %"thang_b.len.1.1"
  %"bin_cmp_val" = icmp eq i32 %".10", 1
  %"if.cond" = icmp ne i1 %"bin_cmp_val", 0
  br i1 %"if.cond", label %"entry.if.then", label %"entry.if.else"
entry.if.then:
  store i32 1, i32* %"iI"
  br label %"entry.if.end"
entry.if.else:
  store i32 2, i32* %"iI"
  br label %"entry.if.end"
entry.if.end:
  br label %"return"
return:
  %".17" = load i32*, i32** %"thang"
  ret i32* %".17"
}

define i32* @"thangg"(i32* %"thang_a", i32** %"thang_b", i32 %"thang_b.len.1")
{
entry:
  %"thangg" = alloca i32*, i32 1
  store i32* null, i32** %"thangg"
  %"thang_a.1" = alloca i32*, i32 1
  store i32* %"thang_a", i32** %"thang_a.1"
  %"thang_b.1" = alloca i32**, i32 1
  store i32** %"thang_b", i32*** %"thang_b.1"
  %"thang_b.len.1.1" = alloca i32, i32 1
  store i32 %"thang_b.len.1", i32* %"thang_b.len.1.1"
  %".9" = load i32, i32* %"thang_b.len.1.1"
  %".10" = alloca i32, i32 1
  store i32 2, i32* %".10"
  br label %"entry.for.cond"
entry.for.cond:
  %"for.idx" = load i32, i32* %".10"
  %".13" = icmp sle i32 %"for.idx", %".9"
  br i1 %".13", label %"entry.for.body", label %"entry.for.end"
entry.for.body:
  %"iI.load" = load i32, i32* %".10"
  store i32 %"iI.load", i32* %".10"
  br label %"entry.for.inc"
entry.for.inc:
  %"for.idx.1" = load i32, i32* %".10"
  %".15" = add i32 %"for.idx.1", 1
  store i32 %".15", i32* %".10"
  br label %"entry.for.cond"
entry.for.end:
  br label %"return"
return:
  %".21" = load i32*, i32** %"thangg"
  ret i32* %".21"
}

define i32* @"thanggg"(i32* %"thang_a", i32** %"thang_b", i32 %"thang_b.len.1")
{
entry:
  %"thanggg" = alloca i32*, i32 1
  store i32* null, i32** %"thanggg"
  %"thang_a.1" = alloca i32*, i32 1
  store i32* %"thang_a", i32** %"thang_a.1"
  %"thang_b.1" = alloca i32**, i32 1
  store i32** %"thang_b", i32*** %"thang_b.1"
  %"thang_b.len.1.1" = alloca i32, i32 1
  store i32 %"thang_b.len.1", i32* %"thang_b.len.1.1"
  %"iI" = alloca i32, i32 1
  store i32 0, i32* %"iI"
  br label %"entry.for.cond"
entry.for.cond:
  %"iI.load" = load i32, i32* %"iI"
  %"bin_cmp_val" = icmp slt i32 %"iI.load", 10
  %"while.cond" = icmp ne i1 %"bin_cmp_val", 0
  br i1 %"while.cond", label %"entry.for.body", label %"entry.for.end"
entry.for.body:
  %"iI.load.1" = load i32, i32* %"iI"
  %"bin_add_val" = add i32 %"iI.load.1", 1
  store i32 %"bin_add_val", i32* %"iI"
  br label %"entry.for.cond"
entry.for.end:
  br label %"return"
return:
  %".15" = load i32*, i32** %"thanggg"
  ret i32* %".15"
}

declare i32* @"than"(i32* %"thang_a", i32** %"thangb", i32 %"thangb.len.1", i32 %"thang_c")
