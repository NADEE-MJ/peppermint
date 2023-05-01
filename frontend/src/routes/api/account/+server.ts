import { fast } from '$lib/fast';
import { redirect, type RequestHandler, json } from '@sveltejs/kit';

export const GET = (async ({ cookies }) => {
	const token = cookies.get('access_token');
	if (token) {
		const response = await fast.getAllAccountsForUser(token);
		const data = await response.json();
		const paginatedResults = data['paginated_results'];

		if (paginatedResults.length === 0) {
			throw new Error('No accounts found');
		}

		return json({ accounts: paginatedResults });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;

export const DELETE = (async ({ cookies, request }) => {
	const token = cookies.get('access_token');
	const toDelete = await request.json();
	if (token) {
		for (const account of toDelete) {
			const response = await fast.deleteAccount(token, account.id);
			const data = await response.json();
			if (!data?.id) {
				throw new Error(`Unable to delete account with name: ${account.name}`);
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
		const response = await fast.updateAccount(token, toUpdate.id, { name: toUpdate.name, account_type: toUpdate.account_type });
		const data = await response.json();
		if (!data?.id) {
			throw new Error(`Unable to update transaction with name: ${toUpdate.name}`);
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
	const account = { name: toAdd.name, account_type: toAdd.account_type };
	if (token) {
		const response = await fast.createAccount(token, account);
		const data = await response.json();
		if (!data?.id) {
			throw new Error(`Unable to add account with name: ${toAdd.name}`);
		}

		return json({ success: true });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;
