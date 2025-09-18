/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ncruz-ga <ncruz-ga@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/04/22 20:23:21 by ncruz-ga          #+#    #+#             */
/*   Updated: 2024/10/21 19:48:39 by ncruz-ga         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft.h"

char	*ft_strchr(const char *s, int c)
{
	if ((!*s && (char) c == '\0'))
		return ((char *) s);
	while (*s != '\0')
	{
		if (*s == (char) c)
			return ((char *) s);
		s++;
		if (*s == (char) c)
			return ((char *) s);
	}
	return (0);
}
