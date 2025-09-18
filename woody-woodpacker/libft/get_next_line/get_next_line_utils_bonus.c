/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils_bonus.c                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ncruz-ga <ncruz-ga@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/05/30 11:55:39 by ncruz-ga          #+#    #+#             */
/*   Updated: 2024/10/21 19:50:25 by ncruz-ga         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft.h"

size_t	ft_strlen_gnl(const char *str)
{
	unsigned int	i;

	i = 0;
	while (str[i] != '\0')
		i++;
	return (i);
}

void	*ft_calloc_gnl(size_t count, size_t size)
{
	char	*ptr;
	size_t	i;

	ptr = (char *)malloc(count * size);
	if (!ptr)
		return (0);
	i = 0;
	while (i < (count * size))
	{
		ptr[i] = '\0';
		i++;
	}
	return (ptr);
}

char	*ft_strjoin_gnl(char *s1, char *s2)
{
	size_t	s1_len;
	char	*result;
	int		i;

	if (!s1)
	{
		s1 = ft_calloc_gnl(1, sizeof(char));
		if (!s1)
			return (free(s1), s1 = NULL, NULL);
	}
	if (!s2)
		return (free(s1), s1 = NULL, NULL);
	s1_len = ft_strlen_gnl(s1);
	result = (char *)ft_calloc((s1_len + ft_strlen_gnl(s2) + 1), sizeof(char));
	if (!result)
		return (free(s1), s1 = NULL, NULL);
	i = -1;
	while (s1[++i])
		result[i] = s1[i];
	i = -1;
	while (s2[++i])
		result[s1_len + i] = s2[i];
	result[s1_len + i] = '\0';
	return (free(s1), s1 = NULL, result);
}

int	ft_strchr_gnl(const char *s, int c)
{
	int	i;

	i = 0;
	if (!s)
		return (0);
	while (s[i])
	{
		if (s[i] == (char)c)
			return (1);
		i++;
	}
	return (0);
}
