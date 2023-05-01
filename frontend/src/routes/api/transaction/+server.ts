import { fast } from '$lib/fast';
import { redirect, type RequestHandler, json } from '@sveltejs/kit';

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

export const PUT = (async ({ cookies, request }) => {
	const token = cookies.get('access_token');
	const toUpdate = await request.json();
	if (token) {
		const response = await fast.updateTransaction(token, toUpdate.id, { amount: toUpdate.amount, date: toUpdate.date, desc: toUpdate.desc });
		const data = await response.json();
		if (!data?.id) {
			throw new Error(`Unable to update transaction with description: ${toUpdate.description}`);
		}

		return json({ success: true });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;

export const POST = (async ({ cookies, request }) => {
	const token = cookies.get('access_token');
	const toAdd = await request.json();
	const transaction = { desc: toAdd.desc, amount: toAdd.amount, date: toAdd.date };
	if (token) {
		const response = await fast.createTransaction(token, transaction, toAdd.account, toAdd.budget, toAdd.category);
		const data = await response.json();
		if (!data?.id) {
			throw new Error(`Unable to add transaction with description: ${toAdd.desc}`);
		}

		return json({ success: true });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;

export const GET = (async ({ cookies, url }) => {
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
		const response = await fast.getAllTransactionsForUser(token, pageNumber);
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
