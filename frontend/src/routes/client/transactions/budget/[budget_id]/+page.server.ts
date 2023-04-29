import { fail, type Actions, redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { fast } from '$lib/fast';

export const load = (async ({ cookies, params }) => {
	const token = cookies.get('access_token');
	if (token) {
		const response = await fast.getTransactionsByBudget(token, params.budget_id, 1);
		const data = await response.json();
		if (data.length === 0) {
			throw fail(404, { message: 'No transactions found' });
		}

		return { transactions: data };
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies PageServerLoad;

export const actions: Actions = {
	getTransactionsByBudget: async ({ cookies, params, request }) => {
		if (params.budget_id === undefined) {
			return fail(400, { message: 'No budget id provided' });
		}

		const formData = await request.formData();

		const pageNumberString = formData.get('pageNumber');
		let pageNumber: number;
		if (pageNumberString && typeof pageNumberString === 'string') {
			pageNumber = parseInt(pageNumberString);
		} else {
			return fail(400, { message: 'Unable to use page number' });
		}

		const token = cookies.get('access_token');
		if (token) {
			const response = await fast.getTransactionsByBudget(token, params.budget_id, pageNumber);
			const data = await response.json();
			if (data.length === 0) {
				return fail(404, { message: 'No transactions found' });
			}

			return { transactions: data };
		} else {
			//! user is not logged in
			throw redirect(303, '/login');
		}
	}
};
