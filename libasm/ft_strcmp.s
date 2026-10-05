section .text
global ft_strcmp

ft_strcmp:
	xor rcx, rcx
	test rdi, rdi
	jz .s1_null
	test rsi, rsi
	jz .s2_null
	jmp .check

.s1_null:
	xor eax, eax            ; ambos NULL -> 0
	test rsi, rsi
	jz .ret
	mov eax, -1             ; NULL < cadena
.ret:
	ret

.s2_null:
	mov eax, 1              ; cadena > NULL
	ret

.compare:
	mov dl, BYTE [rsi + rcx]
	cmp BYTE [rdi + rcx], dl
	jne .compare_last
.increment:
	inc rcx
.check:
	cmp BYTE [rdi + rcx], 0
	je .compare_last
	cmp BYTE [rsi + rcx], 0
	je .compare_last
	jmp .compare

.compare_last:
	movzx eax, BYTE [rdi + rcx]
	movzx edx, BYTE [rsi + rcx]
	sub   eax, edx
	ret