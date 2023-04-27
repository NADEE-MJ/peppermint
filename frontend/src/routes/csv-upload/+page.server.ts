import { fail, redirect } from '@sveltejs/kit';
import { fast } from '$lib/fast';
import type { Actions } from './$types';

export const actions = {
    uploadFile: async ({ request,  }) => {
        const data = await request.formData();
        console.log('data', data);
        const file = data.get("file");
        console.log(file)
        console.log(await fast.get('test'))
        
        
        return { success:true };
    }
}


