/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap_bonus.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ncruz-ga <ncruz-ga@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/05/04 14:37:34 by ncruz-ga          #+#    #+#             */
/*   Updated: 2024/10/21 19:43:36 by ncruz-ga         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft.h"

t_list	*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
	t_list	*newlist;
	t_list	*actual;
	void	*aux;

	if (!lst)
		return (NULL);
	newlist = 0;
	while (lst != NULL)
	{
		aux = f(lst->content);
		actual = ft_lstnew(aux);
		if (actual != NULL)
		{
			ft_lstadd_back(&newlist, actual);
			lst = lst->next;
		}
		else
		{
			ft_lstclear(&newlist, del);
			del(aux);
			return (0);
		}
	}
	return (newlist);
}
