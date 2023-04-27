import type { RequestHandler } from "@sveltejs/kit";

// import { fast } from '$lib/fast'; //! create a method in fast to logout on backend as well
export const POST: RequestHandler = async ({ request }) => {

	//! need to add token to token blocklist on backend so it cannot be used again
    const data = await request.formData();
    const files = data.getAll('file');
    console.log('data', data);
    console.log('files', files);
    return new Response('test');
};
