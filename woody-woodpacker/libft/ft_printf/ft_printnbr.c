/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printnbr.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ncruz-ga <ncruz-ga@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/07/20 11:01:00 by ncruz-ga          #+#    #+#             */
/*   Updated: 2024/10/21 19:12:24 by ncruz-ga         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_printdec(long long int n)
{
	int		result;
	char	c;

	result = 0;
	if (n < 0)
	{
		result += ft_putchar('-');
		if (result == -1)
			return (-1);
		n = -n;
	}
	if (n > 9)
	{
		result += ft_printdec(n / 10);
		if (result == -1)
			return (-1);
	}
	c = n % 10 + '0';
	result += ft_putchar(c);
	if (result == -1)
		return (-1);
	return (result);
}

int	ft_printunsigned(unsigned long long int n)
{
	int	count;
	int	aux;

	count = 0;
	if (n <= 9)
	{
		aux = ft_putchar(n + '0');
		if (aux == -1)
			return (-1);
		count += aux;
	}
	else
	{
		aux = ft_printunsigned (n / 10);
		if (aux == -1)
			return (-1);
		count += aux;
		aux = ft_printunsigned (n % 10);
		if (aux == -1)
			return (-1);
		count += aux;
	}
	return (count);
}

int	ft_printhexa(unsigned long long n, char c)
{
	int	count;

	count = 0;
	if (n >= 16)
	{
		count += ft_printhexa(n / 16, c);
		if (count == -1)
			return (-1);
	}
	if (c == 'x')
	{
		count += ft_putchar("0123456789abcdef"[n % 16]);
		if (count == -1)
			return (-1);
	}
	else if (c == 'X')
	{
		count += ft_putchar("0123456789ABCDEF"[n % 16]);
		if (count == -1)
			return (-1);
	}
	return (count);
}
