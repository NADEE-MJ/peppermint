import { fast } from '$lib/fast';
import { redirect, type RequestHandler, json } from '@sveltejs/kit';

export const GET = (async ({ cookies, params }) => {
	if (params.budget_id === undefined) {
		throw new Error('No budget id provided');
	}

	let numMonths = 1;
	if (params.num_months !== undefined) {
		numMonths = parseInt(params.num_months);
	}

	const token = cookies.get('access_token');
	if (token) {
		const response = await fast.getTransactionsByBudgetAndNumMonths(token, params.budget_id, numMonths);
		const data = await response.json();

		if (data.length === 0) {
			throw new Error('No transactions found');
		}

		return json({ transactions: data });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;
