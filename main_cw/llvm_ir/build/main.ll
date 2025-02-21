; ModuleID = '/mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/main.cpp'
source_filename = "/mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/main.cpp"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%ld\00", align 1
@.str.2 = private unnamed_addr constant [4 x i8] c"%lf\00", align 1
@.str.3 = private unnamed_addr constant [3 x i8] c"%f\00", align 1
@.str.4 = private unnamed_addr constant [4 x i8] c"%ls\00", align 1
@.str.5 = private unnamed_addr constant [8 x i8] c"C.UTF-8\00", align 1

; Function Attrs: mustprogress noinline optnone uwtable
define dso_local void @PrintI(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  store i32 %0, i32* %2, align 4
  %3 = load i32, i32* %2, align 4
  %4 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 noundef %3)
  ret void
}

declare i32 @printf(i8* noundef, ...) #1

; Function Attrs: mustprogress noinline optnone uwtable
define dso_local void @PrintL(i64 noundef %0) #0 {
  %2 = alloca i64, align 8
  store i64 %0, i64* %2, align 8
  %3 = load i64, i64* %2, align 8
  %4 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i64 noundef %3)
  ret void
}

; Function Attrs: mustprogress noinline optnone uwtable
define dso_local void @PrintD(double noundef %0) #0 {
  %2 = alloca double, align 8
  store double %0, double* %2, align 8
  %3 = load double, double* %2, align 8
  %4 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([4 x i8], [4 x i8]* @.str.2, i64 0, i64 0), double noundef %3)
  ret void
}

; Function Attrs: mustprogress noinline optnone uwtable
define dso_local void @PrintF(float noundef %0) #0 {
  %2 = alloca float, align 4
  store float %0, float* %2, align 4
  %3 = load float, float* %2, align 4
  %4 = fpext float %3 to double
  %5 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([3 x i8], [3 x i8]* @.str.3, i64 0, i64 0), double noundef %4)
  ret void
}

; Function Attrs: mustprogress noinline optnone uwtable
define dso_local void @PrintS(i32* noundef %0) #0 {
  %2 = alloca i32*, align 8
  store i32* %0, i32** %2, align 8
  %3 = load i32*, i32** %2, align 8
  %4 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([4 x i8], [4 x i8]* @.str.4, i64 0, i64 0), i32* noundef %3)
  ret void
}

; Function Attrs: mustprogress noinline nounwind optnone uwtable
define dso_local i32* @StringConcat(i32* noundef %0, i32* noundef %1) #2 {
  %3 = alloca i32*, align 8
  %4 = alloca i32*, align 8
  %5 = alloca i64, align 8
  %6 = alloca i64, align 8
  store i32* %0, i32** %3, align 8
  store i32* %1, i32** %4, align 8
  %7 = load i32*, i32** %3, align 8
  %8 = call i64 @wcslen(i32* noundef %7) #6
  store i64 %8, i64* %5, align 8
  %9 = load i32*, i32** %4, align 8
  %10 = call i64 @wcslen(i32* noundef %9) #6
  store i64 %10, i64* %6, align 8
  %11 = load i32*, i32** %3, align 8
  %12 = bitcast i32* %11 to i8*
  %13 = load i64, i64* %5, align 8
  %14 = load i64, i64* %6, align 8
  %15 = add i64 %13, %14
  %16 = add i64 %15, 1
  %17 = mul i64 %16, 4
  %18 = call i8* @realloc(i8* noundef %12, i64 noundef %17) #7
  %19 = bitcast i8* %18 to i32*
  store i32* %19, i32** %3, align 8
  %20 = load i32*, i32** %3, align 8
  %21 = load i32*, i32** %4, align 8
  %22 = call i32* @wcscat(i32* noundef %20, i32* noundef %21) #7
  ret i32* %22
}

; Function Attrs: nounwind readonly willreturn
declare i64 @wcslen(i32* noundef) #3

; Function Attrs: nounwind
declare i8* @realloc(i8* noundef, i64 noundef) #4

; Function Attrs: nounwind
declare i32* @wcscat(i32* noundef, i32* noundef) #4

; Function Attrs: mustprogress noinline nounwind optnone uwtable
define dso_local i32* @StringCopy(i32* noundef %0) #2 {
  %2 = alloca i32*, align 8
  %3 = alloca i64, align 8
  %4 = alloca i32*, align 8
  store i32* %0, i32** %2, align 8
  %5 = load i32*, i32** %2, align 8
  %6 = call i64 @wcslen(i32* noundef %5) #6
  store i64 %6, i64* %3, align 8
  %7 = load i64, i64* %3, align 8
  %8 = add i64 %7, 1
  %9 = call noalias i8* @calloc(i64 noundef %8, i64 noundef 4) #7
  %10 = bitcast i8* %9 to i32*
  store i32* %10, i32** %4, align 8
  %11 = load i32*, i32** %4, align 8
  %12 = load i32*, i32** %2, align 8
  %13 = load i64, i64* %3, align 8
  %14 = call i32* @wcsncpy(i32* noundef %11, i32* noundef %12, i64 noundef %13) #7
  %15 = load i32*, i32** %4, align 8
  ret i32* %15
}

; Function Attrs: nounwind
declare noalias i8* @calloc(i64 noundef, i64 noundef) #4

; Function Attrs: nounwind
declare i32* @wcsncpy(i32* noundef, i32* noundef, i64 noundef) #4

; Function Attrs: mustprogress noinline norecurse optnone uwtable
define dso_local noundef i32 @main(i32 noundef %0, i8** noundef %1) #5 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i8**, align 8
  %6 = alloca i32**, align 8
  %7 = alloca i32, align 4
  %8 = alloca i64, align 8
  %9 = alloca i64, align 8
  %10 = alloca i32, align 4
  store i32 0, i32* %3, align 4
  store i32 %0, i32* %4, align 4
  store i8** %1, i8*** %5, align 8
  %11 = call i8* @setlocale(i32 noundef 6, i8* noundef getelementptr inbounds ([8 x i8], [8 x i8]* @.str.5, i64 0, i64 0)) #7
  %12 = load i32, i32* %4, align 4
  %13 = sext i32 %12 to i64
  %14 = call noalias i8* @calloc(i64 noundef %13, i64 noundef 8) #7
  %15 = bitcast i8* %14 to i32**
  store i32** %15, i32*** %6, align 8
  store i32 0, i32* %7, align 4
  br label %16

16:                                               ; preds = %60, %2
  %17 = load i32, i32* %7, align 4
  %18 = load i32, i32* %4, align 4
  %19 = icmp slt i32 %17, %18
  br i1 %19, label %20, label %63

20:                                               ; preds = %16
  %21 = load i8**, i8*** %5, align 8
  %22 = load i32, i32* %7, align 4
  %23 = sext i32 %22 to i64
  %24 = getelementptr inbounds i8*, i8** %21, i64 %23
  %25 = load i8*, i8** %24, align 8
  %26 = call i64 @strlen(i8* noundef %25) #6
  store i64 %26, i64* %8, align 8
  %27 = load i64, i64* %8, align 8
  %28 = add i64 %27, 1
  %29 = call noalias i8* @calloc(i64 noundef %28, i64 noundef 4) #7
  %30 = bitcast i8* %29 to i32*
  %31 = load i32**, i32*** %6, align 8
  %32 = load i32, i32* %7, align 4
  %33 = sext i32 %32 to i64
  %34 = getelementptr inbounds i32*, i32** %31, i64 %33
  store i32* %30, i32** %34, align 8
  store i64 0, i64* %9, align 8
  br label %35

35:                                               ; preds = %56, %20
  %36 = load i64, i64* %9, align 8
  %37 = load i64, i64* %8, align 8
  %38 = icmp ult i64 %36, %37
  br i1 %38, label %39, label %59

39:                                               ; preds = %35
  %40 = load i8**, i8*** %5, align 8
  %41 = load i32, i32* %7, align 4
  %42 = sext i32 %41 to i64
  %43 = getelementptr inbounds i8*, i8** %40, i64 %42
  %44 = load i8*, i8** %43, align 8
  %45 = load i64, i64* %9, align 8
  %46 = getelementptr inbounds i8, i8* %44, i64 %45
  %47 = load i8, i8* %46, align 1
  %48 = sext i8 %47 to i32
  %49 = load i32**, i32*** %6, align 8
  %50 = load i32, i32* %7, align 4
  %51 = sext i32 %50 to i64
  %52 = getelementptr inbounds i32*, i32** %49, i64 %51
  %53 = load i32*, i32** %52, align 8
  %54 = load i64, i64* %9, align 8
  %55 = getelementptr inbounds i32, i32* %53, i64 %54
  store i32 %48, i32* %55, align 4
  br label %56

56:                                               ; preds = %39
  %57 = load i64, i64* %9, align 8
  %58 = add i64 %57, 1
  store i64 %58, i64* %9, align 8
  br label %35, !llvm.loop !6

59:                                               ; preds = %35
  br label %60

60:                                               ; preds = %59
  %61 = load i32, i32* %7, align 4
  %62 = add nsw i32 %61, 1
  store i32 %62, i32* %7, align 4
  br label %16, !llvm.loop !8

63:                                               ; preds = %16
  %64 = load i32**, i32*** %6, align 8
  %65 = load i32, i32* %4, align 4
  %66 = call i32* @Main(i32** noundef %64, i32 noundef %65)
  store i32 0, i32* %10, align 4
  br label %67

67:                                               ; preds = %78, %63
  %68 = load i32, i32* %10, align 4
  %69 = load i32, i32* %4, align 4
  %70 = icmp slt i32 %68, %69
  br i1 %70, label %71, label %81

71:                                               ; preds = %67
  %72 = load i32**, i32*** %6, align 8
  %73 = load i32, i32* %10, align 4
  %74 = sext i32 %73 to i64
  %75 = getelementptr inbounds i32*, i32** %72, i64 %74
  %76 = load i32*, i32** %75, align 8
  %77 = bitcast i32* %76 to i8*
  call void @free(i8* noundef %77) #7
  br label %78

78:                                               ; preds = %71
  %79 = load i32, i32* %10, align 4
  %80 = add nsw i32 %79, 1
  store i32 %80, i32* %10, align 4
  br label %67, !llvm.loop !9

81:                                               ; preds = %67
  %82 = load i32**, i32*** %6, align 8
  %83 = bitcast i32** %82 to i8*
  call void @free(i8* noundef %83) #7
  ret i32 0
}

; Function Attrs: nounwind
declare i8* @setlocale(i32 noundef, i8* noundef) #4

; Function Attrs: nounwind readonly willreturn
declare i64 @strlen(i8* noundef) #3

declare i32* @Main(i32** noundef, i32 noundef) #1

; Function Attrs: nounwind
declare void @free(i8* noundef) #4

attributes #0 = { mustprogress noinline optnone uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { mustprogress noinline nounwind optnone uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { nounwind readonly willreturn "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { nounwind "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #5 = { mustprogress noinline norecurse optnone uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #6 = { nounwind readonly willreturn }
attributes #7 = { nounwind }

!llvm.module.flags = !{!0, !1, !2, !3, !4}
!llvm.ident = !{!5}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!2 = !{i32 7, !"PIE Level", i32 2}
!3 = !{i32 7, !"uwtable", i32 1}
!4 = !{i32 7, !"frame-pointer", i32 2}
!5 = !{!"Ubuntu clang version 14.0.0-1ubuntu1.1"}
!6 = distinct !{!6, !7}
!7 = !{!"llvm.loop.mustprogress"}
!8 = distinct !{!8, !7}
!9 = distinct !{!9, !7}
