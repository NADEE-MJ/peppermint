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
