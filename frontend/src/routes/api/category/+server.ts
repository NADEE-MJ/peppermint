import { fast } from '$lib/fast';
import { redirect, type RequestHandler, json } from '@sveltejs/kit';

export const GET = (async ({ cookies }) => {
	const token = cookies.get('access_token');
	if (token) {
		const response = await fast.getAllCategoriesForUser(token);
		const data = await response.json();
		const categories = data['paginated_results'];
		const totalPages = data['total_pages'];
		if (categories.length === 0 || totalPages == 0) {
			throw new Error('No categories found');
		} else if (totalPages > 1) {
			throw new Error('Something went wrong when getting categories');
		}

		return json({ categories });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;

export const DELETE = (async ({ cookies, request }) => {
	const token = cookies.get('access_token');
	const toDelete = await request.json();
	if (token) {
		for (const category of toDelete) {
			const response = await fast.deleteCategory(token, category.id);
			const data = await response.json();
			if (!data?.id) {
				throw new Error(`Unable to delete category with name: ${category.name}`);
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
		const response = await fast.updateCategory(token, toUpdate.id, { name: toUpdate.name, amount: toUpdate.amount, desc: toUpdate.desc });
		const data = await response.json();
		if (!data?.id) {
			throw new Error(`Unable to update category with name: ${toUpdate.name}`);
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
	const category = { name: toAdd.name, amount: toAdd.amount, desc: toAdd.desc };
	if (token) {
		const response = await fast.createCategory(token, category, toAdd.budget);
		const data = await response.json();
		if (!data?.id) {
			throw new Error(`Unable to add category with name: ${toAdd.name}`);
		}

		return json({ success: true });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;
