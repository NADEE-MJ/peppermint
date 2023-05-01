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
		const response = await fast.getFiltersForUser(token, pageNumber);
		const data = await response.json();
		const paginatedResults = data['paginated_results'];
		const totalPages = data['total_pages'];

		if (paginatedResults.length === 0) {
			throw new Error('No accounts found');
		}

		return json({ filters: paginatedResults, totalPages: totalPages });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;

export const DELETE = (async ({ cookies, request }) => {
	const token = cookies.get('access_token');
	const toDelete = await request.json();
	if (token) {
		for (const filter of toDelete) {
			const response = await fast.deleteFilter(token, filter.id);
			const data = await response.json();
			if (!data?.id) {
				throw new Error(`Unable to delete filter with filter by: ${filter.filter_by}`);
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
		const response = await fast.updateFilter(token, toUpdate.id, { filter_by: toUpdate.filter_by });
		const data = await response.json();
		if (!data?.id) {
			throw new Error(`Unable to update filter with filter by: ${toUpdate.filter_by}`);
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
	const filter = { filter_by: toAdd.filter_by };
	if (token) {
		const response = await fast.createFilter(token, filter, toAdd.category);
		const data = await response.json();
		if (!data?.id) {
			throw new Error(`Unable to add filter with filter by: ${toAdd.filter_by}`);
		}

		return json({ success: true });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;
