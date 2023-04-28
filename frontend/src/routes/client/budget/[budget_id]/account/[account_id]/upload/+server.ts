import { fast } from '$lib/fast';
import { json, type RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request, cookies, params }) => {
	const token = cookies.get('access_token');
	if (token) {
		const data = await request.json();
		const { file, mapping } = data;
		if (!file || !mapping) {
			throw new Error('Missing file or mapping');
		}

		let budget_id: number;
		if (typeof params.budget_id === 'string') {
			budget_id = parseInt(params.budget_id);
		} else {
			throw new Error('Budget Id must be and Integer');
		}

		let account_id: number;
		if (typeof params.account_id === 'string') {
			account_id = parseInt(params.account_id);
		} else {
			throw new Error('Budget Id must be and Integer');
		}

		const res = await fast.parseTransactions(token, mapping, file, budget_id, account_id);

		return json(await res.json());
	} else {
		throw new Error('You are not logged in');
	}
};
