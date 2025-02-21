	.text
	.file	"test5.ll"
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
	.globl	thang                           # -- Begin function thang
	.p2align	4, 0x90
	.type	thang,@function
thang:                                  # @thang
	.cfi_startproc
# %bb.0:                                # %entry
	movq	$0, -32(%rsp)
	movq	%rdi, -8(%rsp)
	movq	%rsi, -16(%rsp)
	movl	%edx, -20(%rsp)
	movl	$0, -36(%rsp)
	cmpl	$1, %edx
	jne	.LBB1_2
# %bb.1:                                # %entry.if.then
	movl	$1, -36(%rsp)
	movq	-32(%rsp), %rax
	retq
.LBB1_2:                                # %entry.if.else
	movl	$2, -36(%rsp)
	movq	-32(%rsp), %rax
	retq
.Lfunc_end1:
	.size	thang, .Lfunc_end1-thang
	.cfi_endproc
                                        # -- End function
	.globl	thangg                          # -- Begin function thangg
	.p2align	4, 0x90
	.type	thangg,@function
thangg:                                 # @thangg
	.cfi_startproc
# %bb.0:                                # %entry
	movq	$0, -32(%rsp)
	movq	%rdi, -8(%rsp)
	movq	%rsi, -16(%rsp)
	movl	%edx, -20(%rsp)
	movl	$2, -36(%rsp)
	cmpl	%edx, -36(%rsp)
	jg	.LBB2_3
	.p2align	4, 0x90
.LBB2_2:                                # %entry.for.body
                                        # =>This Inner Loop Header: Depth=1
	incl	-36(%rsp)
	cmpl	%edx, -36(%rsp)
	jle	.LBB2_2
.LBB2_3:                                # %entry.for.end
	movq	-32(%rsp), %rax
	retq
.Lfunc_end2:
	.size	thangg, .Lfunc_end2-thangg
	.cfi_endproc
                                        # -- End function
	.globl	thanggg                         # -- Begin function thanggg
	.p2align	4, 0x90
	.type	thanggg,@function
thanggg:                                # @thanggg
	.cfi_startproc
# %bb.0:                                # %entry
	movq	$0, -32(%rsp)
	movq	%rdi, -8(%rsp)
	movq	%rsi, -16(%rsp)
	movl	%edx, -20(%rsp)
	movl	$0, -36(%rsp)
	cmpl	$9, -36(%rsp)
	jg	.LBB3_3
	.p2align	4, 0x90
.LBB3_2:                                # %entry.for.body
                                        # =>This Inner Loop Header: Depth=1
	incl	-36(%rsp)
	cmpl	$9, -36(%rsp)
	jle	.LBB3_2
.LBB3_3:                                # %entry.for.end
	movq	-32(%rsp), %rax
	retq
.Lfunc_end3:
	.size	thanggg, .Lfunc_end3-thanggg
	.cfi_endproc
                                        # -- End function
	.section	.init_array,"aw",@init_array
	.p2align	3
	.quad	variable_decl_constructor
	.section	".note.GNU-stack","",@progbits
