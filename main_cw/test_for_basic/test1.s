	.text
	.file	"test1.ll"
	.globl	variable_decl_constructor       # -- Begin function variable_decl_constructor
	.p2align	4, 0x90
	.type	variable_decl_constructor,@function
variable_decl_constructor:              # @variable_decl_constructor
	.cfi_startproc
# %bb.0:                                # %entry
	retq
.Lfunc_end0:
	.size	variable_decl_constructor, .Lfunc_end0-variable_decl_constructor
	.cfi_endproc
                                        # -- End function
	.globl	SumArray                        # -- Begin function SumArray
	.p2align	4, 0x90
	.type	SumArray,@function
SumArray:                               # @SumArray
	.cfi_startproc
# %bb.0:                                # %entry
	movq	$0, -24(%rsp)
	movq	%rdi, -16(%rsp)
	movl	%esi, -4(%rsp)
	movl	$1, -28(%rsp)
	cmpl	%esi, -28(%rsp)
	jg	.LBB1_3
	.p2align	4, 0x90
.LBB1_2:                                # %entry.for.body
                                        # =>This Inner Loop Header: Depth=1
	movsd	-24(%rsp), %xmm0                # xmm0 = mem[0],zero
	movl	-28(%rsp), %eax
	leal	-1(%rax), %ecx
	movq	-16(%rsp), %rdx
	movslq	%ecx, %rcx
	addsd	(%rdx,%rcx,8), %xmm0
	movsd	%xmm0, -24(%rsp)
	incl	%eax
	movl	%eax, -28(%rsp)
	cmpl	%esi, -28(%rsp)
	jle	.LBB1_2
.LBB1_3:                                # %entry.for.end
	movsd	-24(%rsp), %xmm0                # xmm0 = mem[0],zero
	retq
.Lfunc_end1:
	.size	SumArray, .Lfunc_end1-SumArray
	.cfi_endproc
                                        # -- End function
	.globl	Polynom                         # -- Begin function Polynom
	.p2align	4, 0x90
	.type	Polynom,@function
Polynom:                                # @Polynom
	.cfi_startproc
# %bb.0:                                # %entry
	movl	$0, -24(%rsp)
	movss	%xmm0, -20(%rsp)
	movq	%rdi, -16(%rsp)
	movl	%esi, -4(%rsp)
	movl	$1, -28(%rsp)
	cmpl	%esi, -28(%rsp)
	jg	.LBB2_3
	.p2align	4, 0x90
.LBB2_2:                                # %entry.for.body
                                        # =>This Inner Loop Header: Depth=1
	movss	-24(%rsp), %xmm0                # xmm0 = mem[0],zero,zero,zero
	mulss	-20(%rsp), %xmm0
	movl	-28(%rsp), %eax
	leal	-1(%rax), %ecx
	movq	-16(%rsp), %rdx
	movslq	%ecx, %rcx
	addss	(%rdx,%rcx,4), %xmm0
	movss	%xmm0, -24(%rsp)
	incl	%eax
	movl	%eax, -28(%rsp)
	cmpl	%esi, -28(%rsp)
	jle	.LBB2_2
.LBB2_3:                                # %entry.for.end
	movss	-24(%rsp), %xmm0                # xmm0 = mem[0],zero,zero,zero
	retq
.Lfunc_end2:
	.size	Polynom, .Lfunc_end2-Polynom
	.cfi_endproc
                                        # -- End function
	.globl	Polynom1111                     # -- Begin function Polynom1111
	.p2align	4, 0x90
	.type	Polynom1111,@function
Polynom1111:                            # @Polynom1111
	.cfi_startproc
# %bb.0:                                # %entry
	subq	$40, %rsp
	.cfi_def_cfa_offset 48
	movl	$0, 20(%rsp)
	movss	%xmm0, 16(%rsp)
	movl	$1, 12(%rsp)
	cmpl	$4, 12(%rsp)
	jg	.LBB3_3
	.p2align	4, 0x90
.LBB3_2:                                # %entry.for.body
                                        # =>This Inner Loop Header: Depth=1
	movl	12(%rsp), %eax
	leal	-1(%rax), %ecx
	movslq	%ecx, %rcx
	movl	$1065353216, 24(%rsp,%rcx,4)    # imm = 0x3F800000
	incl	%eax
	movl	%eax, 12(%rsp)
	cmpl	$4, 12(%rsp)
	jle	.LBB3_2
.LBB3_3:                                # %entry.for.end
	movss	16(%rsp), %xmm0                 # xmm0 = mem[0],zero,zero,zero
	leaq	24(%rsp), %rdi
	movl	$4, %esi
	callq	Polynom@PLT
	movss	%xmm0, 20(%rsp)
	addq	$40, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end3:
	.size	Polynom1111, .Lfunc_end3-Polynom1111
	.cfi_endproc
                                        # -- End function
	.globl	Fibonacci                       # -- Begin function Fibonacci
	.p2align	4, 0x90
	.type	Fibonacci,@function
Fibonacci:                              # @Fibonacci
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$32, %rsp
	movq	%rdi, -16(%rbp)
	movl	%esi, -20(%rbp)
	movl	%esi, -4(%rbp)
	testl	%esi, %esi
	jle	.LBB4_2
# %bb.1:                                # %entry.if.then
	movq	-16(%rbp), %rax
	movq	$1, (%rax)
.LBB4_2:                                # %entry.if.end
	cmpl	$2, -4(%rbp)
	jl	.LBB4_4
# %bb.3:                                # %entry.if.end.if.then
	movq	-16(%rbp), %rax
	movq	$1, 8(%rax)
.LBB4_4:                                # %entry.if.end.if.end
	movq	%rsp, %rcx
	leaq	-16(%rcx), %rax
	movq	%rax, %rsp
	movl	$3, -16(%rcx)
	.p2align	4, 0x90
.LBB4_5:                                # %entry.if.end.if.end.for.cond
                                        # =>This Inner Loop Header: Depth=1
	movl	(%rax), %ecx
	cmpl	-4(%rbp), %ecx
	jg	.LBB4_7
# %bb.6:                                # %entry.if.end.if.end.for.body
                                        #   in Loop: Header=BB4_5 Depth=1
	movl	(%rax), %ecx
	leal	-1(%rcx), %edx
	movq	-16(%rbp), %rsi
	movslq	%edx, %rdx
	leal	-2(%rcx), %edi
	movslq	%edi, %rdi
	movq	(%rsi,%rdi,8), %rdi
	addl	$-3, %ecx
	movslq	%ecx, %rcx
	addq	(%rsi,%rcx,8), %rdi
	movq	%rdi, (%rsi,%rdx,8)
	incl	(%rax)
	jmp	.LBB4_5
.LBB4_7:                                # %entry.if.end.if.end.for.end
	movq	%rbp, %rsp
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end4:
	.size	Fibonacci, .Lfunc_end4-Fibonacci
	.cfi_endproc
                                        # -- End function
	.globl	Join                            # -- Begin function Join
	.p2align	4, 0x90
	.type	Join,@function
Join:                                   # @Join
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$32, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movq	$0, -24(%rbp)
	movq	%rdi, -48(%rbp)
	movq	%rsi, -40(%rbp)
	movl	%edx, -28(%rbp)
	testl	%edx, %edx
	jle	.LBB5_2
# %bb.1:                                # %entry.if.then
	movq	-40(%rbp), %rax
	movq	(%rax), %rdi
	callq	StringCopy@PLT
	jmp	.LBB5_3
.LBB5_2:                                # %entry.if.else
	movq	.str.1@GOTPCREL(%rip), %rax
.LBB5_3:                                # %entry.if.end
	movq	%rax, -24(%rbp)
	movl	-28(%rbp), %r14d
	movq	%rsp, %rax
	leaq	-16(%rax), %rbx
	movq	%rbx, %rsp
	movl	$2, -16(%rax)
	cmpl	%r14d, (%rbx)
	jg	.LBB5_6
	.p2align	4, 0x90
.LBB5_5:                                # %entry.if.end.for.body
                                        # =>This Inner Loop Header: Depth=1
	movq	-24(%rbp), %rdi
	movq	-48(%rbp), %rsi
	callq	StringConcat@PLT
	movl	(%rbx), %ecx
	decl	%ecx
	movq	-40(%rbp), %rdx
	movslq	%ecx, %rcx
	movq	(%rdx,%rcx,8), %rsi
	movq	%rax, %rdi
	callq	StringConcat@PLT
	movq	%rax, %rdi
	callq	StringCopy@PLT
	movq	%rax, -24(%rbp)
	incl	(%rbx)
	cmpl	%r14d, (%rbx)
	jle	.LBB5_5
.LBB5_6:                                # %entry.if.end.for.end
	movq	-24(%rbp), %rax
	leaq	-16(%rbp), %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end5:
	.size	Join, .Lfunc_end5-Join
	.cfi_endproc
                                        # -- End function
	.globl	Main                            # -- Begin function Main
	.p2align	4, 0x90
	.type	Main,@function
Main:                                   # @Main
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$1632, %rsp                     # imm = 0x660
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdi, -48(%rbp)
	movl	%esi, -40(%rbp)
	movq	.str.2@GOTPCREL(%rip), %rdi
	callq	PrintS@PLT
	movq	.str.3@GOTPCREL(%rip), %rdi
	movq	-48(%rbp), %rsi
	movl	-40(%rbp), %edx
	callq	Join@PLT
	movq	%rax, %rdi
	callq	PrintS@PLT
	movq	.str.4@GOTPCREL(%rip), %rdi
	callq	PrintS@PLT
	leaq	-848(%rbp), %rdi
	movl	$100, %esi
	callq	Fibonacci@PLT
	movq	.str.5@GOTPCREL(%rip), %rdi
	callq	PrintS@PLT
	movq	-456(%rbp), %rdi
	callq	PrintL@PLT
	movq	.str.6@GOTPCREL(%rip), %rdi
	callq	PrintS@PLT
	movq	.str.7@GOTPCREL(%rip), %rdi
	callq	PrintS@PLT
	movl	$-50, -36(%rbp)
	movq	.str.8@GOTPCREL(%rip), %r14
	movq	.str.9@GOTPCREL(%rip), %r15
	movq	.str.10@GOTPCREL(%rip), %r12
	cmpl	$50, -36(%rbp)
	jg	.LBB6_3
	.p2align	4, 0x90
.LBB6_2:                                # %entry.for.body
                                        # =>This Inner Loop Header: Depth=1
	movq	%rsp, %rbx
	leaq	-16(%rbx), %rsp
	xorps	%xmm0, %xmm0
	cvtsi2ssl	-36(%rbp), %xmm0
	callq	Polynom1111@PLT
	movss	%xmm0, -16(%rbx)
	movq	%r14, %rdi
	callq	PrintS@PLT
	movl	-36(%rbp), %edi
	callq	PrintI@PLT
	movq	%r15, %rdi
	callq	PrintS@PLT
	movss	-16(%rbx), %xmm0                # xmm0 = mem[0],zero,zero,zero
	callq	PrintF@PLT
	movq	%r12, %rdi
	callq	PrintS@PLT
	movl	-36(%rbp), %eax
	leal	50(%rax), %ecx
	movslq	%ecx, %rcx
	movss	-16(%rbx), %xmm0                # xmm0 = mem[0],zero,zero,zero
	cvtss2sd	%xmm0, %xmm0
	movsd	%xmm0, -1656(%rbp,%rcx,8)
	incl	%eax
	movl	%eax, -36(%rbp)
	cmpl	$50, -36(%rbp)
	jle	.LBB6_2
.LBB6_3:                                # %entry.for.end
	movq	.str.11@GOTPCREL(%rip), %rdi
	callq	PrintS@PLT
	leaq	-1656(%rbp), %rdi
	movl	$101, %esi
	callq	SumArray@PLT
	callq	PrintD@PLT
	movq	.str.12@GOTPCREL(%rip), %rdi
	callq	PrintS@PLT
	leaq	-32(%rbp), %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end6:
	.size	Main, .Lfunc_end6-Main
	.cfi_endproc
                                        # -- End function
	.section	.init_array,"aw",@init_array
	.p2align	3
	.quad	variable_decl_constructor
	.type	.str.1,@object                  # @.str.1
	.bss
	.globl	.str.1
	.p2align	2
.str.1:
	.zero	4
	.size	.str.1, 4

	.type	.str.2,@object                  # @.str.2
	.data
	.globl	.str.2
	.p2align	4
.str.2:
	.long	1040                            # 0x410
	.long	1088                            # 0x440
	.long	1075                            # 0x433
	.long	1091                            # 0x443
	.long	1084                            # 0x43c
	.long	1077                            # 0x435
	.long	1085                            # 0x43d
	.long	1090                            # 0x442
	.long	1099                            # 0x44b
	.long	32                              # 0x20
	.long	1087                            # 0x43f
	.long	1088                            # 0x440
	.long	1086                            # 0x43e
	.long	1075                            # 0x433
	.long	1088                            # 0x440
	.long	1072                            # 0x430
	.long	1084                            # 0x43c
	.long	1084                            # 0x43c
	.long	1099                            # 0x44b
	.long	58                              # 0x3a
	.long	32                              # 0x20
	.long	0                               # 0x0
	.size	.str.2, 88

	.type	.str.3,@object                  # @.str.3
	.globl	.str.3
	.p2align	2
.str.3:
	.long	44                              # 0x2c
	.long	32                              # 0x20
	.long	0                               # 0x0
	.size	.str.3, 12

	.type	.str.4,@object                  # @.str.4
	.globl	.str.4
	.p2align	2
.str.4:
	.long	10                              # 0xa
	.long	0                               # 0x0
	.size	.str.4, 8

	.type	.str.5,@object                  # @.str.5
	.globl	.str.5
	.p2align	4
.str.5:
	.long	53                              # 0x35
	.long	48                              # 0x30
	.long	45                              # 0x2d
	.long	1077                            # 0x435
	.long	32                              # 0x20
	.long	1095                            # 0x447
	.long	1080                            # 0x438
	.long	1089                            # 0x441
	.long	1083                            # 0x43b
	.long	1086                            # 0x43e
	.long	32                              # 0x20
	.long	1060                            # 0x424
	.long	1080                            # 0x438
	.long	1073                            # 0x431
	.long	1086                            # 0x43e
	.long	1085                            # 0x43d
	.long	1072                            # 0x430
	.long	1095                            # 0x447
	.long	1095                            # 0x447
	.long	1080                            # 0x438
	.long	32                              # 0x20
	.long	8212                            # 0x2014
	.long	32                              # 0x20
	.long	0                               # 0x0
	.size	.str.5, 96

	.type	.str.6,@object                  # @.str.6
	.globl	.str.6
	.p2align	2
.str.6:
	.long	10                              # 0xa
	.long	0                               # 0x0
	.size	.str.6, 8

	.type	.str.7,@object                  # @.str.7
	.globl	.str.7
	.p2align	4
.str.7:
	.long	1058                            # 0x422
	.long	1072                            # 0x430
	.long	1073                            # 0x431
	.long	1083                            # 0x43b
	.long	1080                            # 0x438
	.long	1094                            # 0x446
	.long	1072                            # 0x430
	.long	32                              # 0x20
	.long	1079                            # 0x437
	.long	1085                            # 0x43d
	.long	1072                            # 0x430
	.long	1095                            # 0x447
	.long	1077                            # 0x435
	.long	1085                            # 0x43d
	.long	1080                            # 0x438
	.long	1081                            # 0x439
	.long	32                              # 0x20
	.long	1092                            # 0x444
	.long	1091                            # 0x443
	.long	1085                            # 0x43d
	.long	1082                            # 0x43a
	.long	1094                            # 0x446
	.long	1080                            # 0x438
	.long	1080                            # 0x438
	.long	32                              # 0x20
	.long	121                             # 0x79
	.long	32                              # 0x20
	.long	61                              # 0x3d
	.long	32                              # 0x20
	.long	120                             # 0x78
	.long	179                             # 0xb3
	.long	32                              # 0x20
	.long	43                              # 0x2b
	.long	32                              # 0x20
	.long	120                             # 0x78
	.long	178                             # 0xb2
	.long	32                              # 0x20
	.long	43                              # 0x2b
	.long	32                              # 0x20
	.long	120                             # 0x78
	.long	32                              # 0x20
	.long	43                              # 0x2b
	.long	32                              # 0x20
	.long	49                              # 0x31
	.long	58                              # 0x3a
	.long	10                              # 0xa
	.long	0                               # 0x0
	.size	.str.7, 188

	.type	.str.8,@object                  # @.str.8
	.globl	.str.8
	.p2align	4
.str.8:
	.long	120                             # 0x78
	.long	32                              # 0x20
	.long	61                              # 0x3d
	.long	32                              # 0x20
	.long	0                               # 0x0
	.size	.str.8, 20

	.type	.str.9,@object                  # @.str.9
	.globl	.str.9
	.p2align	4
.str.9:
	.long	44                              # 0x2c
	.long	32                              # 0x20
	.long	121                             # 0x79
	.long	32                              # 0x20
	.long	61                              # 0x3d
	.long	32                              # 0x20
	.long	0                               # 0x0
	.size	.str.9, 28

	.type	.str.10,@object                 # @.str.10
	.globl	.str.10
	.p2align	2
.str.10:
	.long	10                              # 0xa
	.long	0                               # 0x0
	.size	.str.10, 8

	.type	.str.11,@object                 # @.str.11
	.globl	.str.11
	.p2align	4
.str.11:
	.long	1057                            # 0x421
	.long	1091                            # 0x443
	.long	1084                            # 0x43c
	.long	1084                            # 0x43c
	.long	1072                            # 0x430
	.long	32                              # 0x20
	.long	1087                            # 0x43f
	.long	1077                            # 0x435
	.long	1088                            # 0x440
	.long	1077                            # 0x435
	.long	1095                            # 0x447
	.long	1080                            # 0x438
	.long	1089                            # 0x441
	.long	1083                            # 0x43b
	.long	1077                            # 0x435
	.long	1085                            # 0x43d
	.long	1085                            # 0x43d
	.long	1099                            # 0x44b
	.long	1093                            # 0x445
	.long	32                              # 0x20
	.long	1079                            # 0x437
	.long	1085                            # 0x43d
	.long	1072                            # 0x430
	.long	1095                            # 0x447
	.long	1077                            # 0x435
	.long	1085                            # 0x43d
	.long	1080                            # 0x438
	.long	1081                            # 0x439
	.long	32                              # 0x20
	.long	121                             # 0x79
	.long	58                              # 0x3a
	.long	32                              # 0x20
	.long	0                               # 0x0
	.size	.str.11, 132

	.type	.str.12,@object                 # @.str.12
	.globl	.str.12
	.p2align	2
.str.12:
	.long	10                              # 0xa
	.long	0                               # 0x0
	.size	.str.12, 8

	.section	".note.GNU-stack","",@progbits
