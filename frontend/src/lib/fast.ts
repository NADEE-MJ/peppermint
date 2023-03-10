import { FAST_URL } from '$env/static/private';

export class fast {
    private static fastURL = FAST_URL;

    static async get(url: string, token: string | null = null) : Promise<Response> {
        let headers = undefined
        if(token) {
            headers = {'Authorization': `Bearer ${token}`}
        }
        const response = await fetch(`${fast.fastURL}/${url}`, {method: 'GET', headers: headers})
        return response;
    }

    static async post(url: string, body: string, token: string | null = null) : Promise<Response> {
        const headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer null'}
        if(token) {
            headers.Authorization = `Bearer ${token}`
        }
        const response = await fetch(`${fast.fastURL}/${url}`, {body: body, method: 'POST', headers: headers})
        return response;
    }

    static async put(url: string, body: string, token: string | null = null) : Promise<Response> {
        const headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer null'}
        if(token) {
            headers.Authorization = `Bearer ${token}`
        }
        const response = await fetch(`${fast.fastURL}/${url}`, {body: body, method: 'PUT', headers: headers})
        return response;
    }

    static async login(email: string, password: string) : Promise<Response> {
        const body = {email: email, password: password}
        const response = await fast.post('login/access-token', JSON.stringify(body))
        return response;
    }

    static async getCurrentUser(token: string) : Promise<Response> {
        const response = await fast.get('users/me', token)
        return response;
    }

    static async updateCurrentUser(token: string, userUpdate: userUpdate) : Promise<Response> {
        const response = await fast.put('users/me', JSON.stringify(userUpdate), token)
        return response;
    }
}

type userUpdate = {
    email: string | null,
    full_name: string | null,
    password: string | null,
    passwordConfirm: string | null
}
