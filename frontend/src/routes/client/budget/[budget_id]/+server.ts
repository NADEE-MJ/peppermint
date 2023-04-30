import { fast } from '$lib/fast';
import { redirect, type RequestHandler, json } from '@sveltejs/kit';

export const GET = (async ({ cookies, params, url }) => {
	if (params.budget_id === undefined) {
		//? maybe can check if this is null and get for the user instead and redirect them
		throw new Error('No budget id provided');
	}

	const searchParams = url.searchParams;
	const pageNumberString = searchParams.get('page');
	let pageNumber: number;
	if (pageNumberString && typeof pageNumberString === 'string') {
		pageNumber = parseInt(pageNumberString);
	} else {
		throw new Error('Unable to use page number');
	}

	const token = cookies.get('access_token');
	if (token) {
		const response = await fast.getTransactionsByBudget(token, params.budget_id, pageNumber);
		const data = await response.json();
		const paginatedResults = data['paginated_results'];
		const totalPages = data['total_pages'];

		if (paginatedResults.length === 0) {
			throw new Error('No transactions found');
		}

		return json({ transactions: paginatedResults, totalPages: totalPages });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;

export const DELETE = (async ({ cookies, request }) => {
	const token = cookies.get('access_token');
	const toDelete = await request.json();
	if (token) {
		for (const transaction of toDelete) {
			const response = await fast.deleteTransaction(token, transaction.id);
			const data = await response.json();
			if (!data?.id) {
				throw new Error(`Unable to delete transaction with description: ${transaction.description}`);
			}
		}

		return json({ success: true });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;
