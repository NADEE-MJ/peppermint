import { fast } from '$lib/fast';
import { redirect, type RequestHandler, json } from '@sveltejs/kit';

export const GET = (async ({ cookies }) => {
	const token = cookies.get('access_token');
	if (token) {
		const response = await fast.getAllBudgetsForUser(token);
		const data = await response.json();
		if (data.length === 0) {
			throw new Error('No budgets found');
		}

		return json({ budgets: data });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;

export const PUT = (async ({ cookies, request }) => {
	const token = cookies.get('access_token');
	const toUpdate = await request.json();
	if (token) {
		const response = await fast.updateBudget(token, toUpdate.id, { name: toUpdate.name, amount: toUpdate.amount });
		const data = await response.json();
		console.log(data);
		if (!data?.id) {
			throw new Error(`Unable to update budget with name: ${toUpdate.name}`);
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
	const budget = { name: toAdd.name, amount: toAdd.amount };
	if (token) {
		const response = await fast.createBudget(token, budget);
		const data = await response.json();
		if (!data?.id) {
			throw new Error(`Unable to add budget with name: ${toAdd.name}`);
		}

		return json({ success: true });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;
