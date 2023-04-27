import { fail, type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { UpdateUserValidator } from '$lib/zodValidators';
import { fast } from '$lib/fast';
import { userStore } from '$lib/stores';
import { get } from 'svelte/store';

export const load = (async ({cookies, params}) => {
	const token = cookies.get('access_token');
	if (token) {
		const response = await fast.getTransactionsByBudget(token, params.budget_id, 1);
		const data = await response.json();

		return { transactions: data };
	} else {
		throw fail(400, {message: "bad request"})
	}
}) satisfies PageServerLoad;

export const actions: Actions = {
    getTransactionsByBudget: async ({ cookies, params, request }) => {
		// console.log(typeof params.budget_id);
		const formData = await request.formData();
		console.log(formData)
		const pageNumber = formData.get('pageNumber');
		const token = cookies.get('access_token');
		if (token) {
			const response = await fast.getTransactionsByBudget(token, params.budget_id, pageNumber);
			const data = await response.json();
			// console.log(data);

			return { transactions: data };
		} else {
			throw fail(400, {message: "bad request"})
		}
	}
};
