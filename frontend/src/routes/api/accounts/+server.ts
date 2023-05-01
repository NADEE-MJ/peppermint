import { fast } from '$lib/fast';
import { redirect, type RequestHandler, json } from '@sveltejs/kit';

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
		const response = await fast.getAccountsForUser(token, pageNumber);
		const data = await response.json();
		const paginatedResults = data['paginated_results'];
		const totalPages = data['total_pages'];

		if (paginatedResults.length === 0) {
			throw new Error('No accounts found');
		}

		return json({ accounts: paginatedResults, totalPages: totalPages });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;
