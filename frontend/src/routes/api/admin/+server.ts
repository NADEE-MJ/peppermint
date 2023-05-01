import { fast } from '$lib/fast';
import { redirect, type RequestHandler, json } from '@sveltejs/kit';

export const GET = (async ({ cookies, params, url }) => {
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
		const response = await fast.getAllUsers(token, pageNumber);
		const data = await response.json();
		const paginatedResults = data['paginated_results'];
		const totalPages = data['total_pages'];

		if (paginatedResults.length === 0) {
			throw new Error('No users found');
		}
		return json({ users: paginatedResults, totalPages: totalPages });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;

export const PUT = (async ({ cookies, request }) => {
	const token = cookies.get('access_token');
	const toUpdate = await request.json();
	if (token) {
		const response = await fast.updateUserAsAdmin(token, toUpdate.id, { 
			email: toUpdate.email, full_name: toUpdate.full_name, password: toUpdate.password, is_active: toUpdate.is_active });
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

export const DELETE = (async ({ cookies, request }) => {
	const token = cookies.get('access_token');
	const toDelete = await request.json();
	if (token) {
		for (const user of toDelete) {
			const response = await fast.deleteUser(token, user.id);
			const data = await response.json();
			if (!data?.id) {
				throw new Error(`Unable to delete user with description: ${user.description}`);
			}
		}
		return json({ success: true });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;