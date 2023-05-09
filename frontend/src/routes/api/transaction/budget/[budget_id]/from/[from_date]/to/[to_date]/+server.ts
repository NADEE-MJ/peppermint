import { fast } from '$lib/fast';
import { redirect, type RequestHandler, json } from '@sveltejs/kit';

export const GET = (async ({ cookies, params }) => {
	if (params.budget_id === undefined) {
		throw new Error('No budget id provided');
	}

	if (params.to_date === undefined) {
		throw new Error('No to date provided');
	}

	if (params.from_date === undefined) {
		throw new Error('No from date provided');
	}

	const token = cookies.get('access_token');
	if (token) {
		const response = await fast.getTransactionsByBudgetAndDateRange(token, params.budget_id, params.from_date, params.to_date);
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
