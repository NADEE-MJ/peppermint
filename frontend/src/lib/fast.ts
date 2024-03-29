import { FAST_URL } from '$env/static/private';

export class fast {
	private static fastURL = FAST_URL;

	static async get(url: string, token: string | null = null): Promise<Response> {
		let headers = undefined;
		if (token) {
			headers = { Authorization: `Bearer ${token}` };
		}
		const response = await fetch(`${fast.fastURL}/${url}`, { method: 'GET', headers: headers });
		return response;
	}

	static async post(url: string, body: string, token: string | null = null): Promise<Response> {
		const headers = { 'Content-Type': 'application/json', Authorization: 'Bearer null' };
		if (token) {
			headers.Authorization = `Bearer ${token}`;
		}
		const response = await fetch(`${fast.fastURL}/${url}`, { body: body, method: 'POST', headers: headers });
		return response;
	}

	static async put(url: string, body: string, token: string | null = null): Promise<Response> {
		const headers = { 'Content-Type': 'application/json', Authorization: 'Bearer null' };
		if (token) {
			headers.Authorization = `Bearer ${token}`;
		}
		const response = await fetch(`${fast.fastURL}/${url}`, { body: body, method: 'PUT', headers: headers });
		return response;
	}

	static async delete(url: string, token: string | null = null): Promise<Response> {
		const headers = { Authorization: 'Bearer null' };
		if (token) {
			headers.Authorization = `Bearer ${token}`;
		}
		const response = await fetch(`${fast.fastURL}/${url}`, { method: 'DELETE', headers: headers });
		return response;
	}

	static async login(email: string, password: string): Promise<Response> {
		const body = new URLSearchParams({ username: email, password: password });
		const headers = { 'Content-Type': 'application/x-www-form-urlencoded', Authorization: 'Bearer null' };
		const response = await fetch(`${fast.fastURL}/login/access-token`, { body: body, method: 'POST', headers: headers });
		return response;
	}

	static async magicLink(token: string): Promise<Response> {
		const response = await fetch(`${fast.fastURL}/magic-link?token=${token}`, { method: 'POST' });
		return response;
	}

	static async sendMagicLink(email: string): Promise<Response> {
		const response = await fetch(`${fast.fastURL}/send-magic-link?email=${email}`, { method: 'POST' });
		return response;
	}

	static async signup(email: string, password: string, full_name: string): Promise<Response> {
		const body = JSON.stringify({ email, password, full_name });
		const response = await fast.post('users/open', body);
		return response;
	}

	static async createUserOrAdmin(token: string, userOrAdminCreate: UserOrAdminCreate): Promise<Response> {
		const body = JSON.stringify({ email: userOrAdminCreate.email, password: userOrAdminCreate.password, full_name: userOrAdminCreate.full_name });
		const response = await fast.post(`admin?is_admin=${userOrAdminCreate.isAdmin}`, body, token);
		return response;
	}

	static async getCurrentUser(token: string): Promise<Response> {
		const response = await fast.get('users/me', token);
		return response;
	}

	static async getCurrentAdmin(token: string): Promise<Response> {
		const response = await fast.get('admin', token);
		return response;
	}

	static async updateCurrentUser(token: string, userUpdate: UserUpdate): Promise<Response> {
		const response = await fast.put('users/me', JSON.stringify(userUpdate), token);
		return response;
	}

	static async updateCurrentAdmin(token: string, userUpdate: UserUpdate): Promise<Response> {
		const response = await fast.put('admin', JSON.stringify(userUpdate), token);
		return response;
	}

	static async parseTransactions(token: string, mapping: object, base64String: string, budget_id: number, account_id: number): Promise<Response> {
		const data = JSON.stringify({ mapping, file: base64String });
		const response = await fast.post(`transactions/parse/budget/${budget_id}/account/${account_id}`, data, token);
		return response;
	}

	static async logout(token: string): Promise<Response> {
		const response = await fast.post('logout', JSON.stringify({ token }), token);
		return response;
	}

	static async getAllTransactionsForUser(token: string, page: number): Promise<Response> {
		page = page - 1;
		const response = await fast.get(`transactions?page=${page}`, token);
		return response;
	}

	static async getTransactionsByBudget(token: string, budgetId: string, page: number): Promise<Response> {
		page = page - 1;
		const response = await fast.get(`transactions/budget/${budgetId}?page=${page}`, token);
		return response;
	}

	static async getTransactionsByAccount(token: string, accountId: string, page: number): Promise<Response> {
		page = page - 1;
		const response = await fast.get(`transactions/account/${accountId}?page=${page}`, token);
		return response;
	}

	static async getTransactionsByBudgetAndCategory(token: string, budgetId: string, categoryId: string, page: number): Promise<Response> {
		page = page - 1;
		const response = await fast.get(`transactions/budget/${budgetId}/category/${categoryId}/?page=${page}`, token);
		return response;
	}

	static async getTransactionsByBudgetAndDateRange(token: string, budgetId: string, fromDate: string, toDate: string): Promise<Response> {
		const response = await fast.get(`transactions/budget/${budgetId}/from/${fromDate}/to/${toDate}`, token);
		return response;
	}

	static async deleteTransaction(token: string, transactionId: string): Promise<Response> {
		const response = await fast.delete(`transactions/${transactionId}`, token);
		return response;
	}

	static async updateTransaction(token: string, transactionId: string, transactionUpdate: TransactionUpdate): Promise<Response> {
		const response = await fast.put(`transactions/${transactionId}`, JSON.stringify(transactionUpdate), token);
		return response;
	}

	static async createTransaction(
		token: string,
		transactionCreate: TransactionCreate,
		accountId: number,
		budgetId: number,
		categoryId: number
	): Promise<Response> {
		const response = await fast.post(
			`transactions/budget/${budgetId}/category/${categoryId}/account/${accountId}`,
			JSON.stringify(transactionCreate),
			token
		);
		return response;
	}

	static async getAllBudgetsForUser(token: string): Promise<Response> {
		const response = await fast.get('budgets', token);
		return response;
	}

	static async updateBudget(token: string, budgetId: string, budgetUpdate: BudgetUpdate): Promise<Response> {
		const response = await fast.put(`budgets/${budgetId}`, JSON.stringify(budgetUpdate), token);
		return response;
	}

	static async createBudget(token: string, budgetCreate: BudgetCreate): Promise<Response> {
		const response = await fast.post(`budgets`, JSON.stringify(budgetCreate), token);
		return response;
	}

	static async getAllAccountsForUser(token: string): Promise<Response> {
		const response = await fast.get('accounts?limit=-1', token);
		return response;
	}

	static async getAccountsForUser(token: string, page: number): Promise<Response> {
		page = page - 1;
		const response = await fast.get(`accounts?page=${page}`, token);
		return response;
	}

	static async deleteAccount(token: string, accountId: string): Promise<Response> {
		const response = await fast.delete(`accounts/${accountId}`, token);
		return response;
	}

	static async updateAccount(token: string, accountId: string, accountUpdate: AccountUpdate): Promise<Response> {
		const response = await fast.put(`accounts/${accountId}`, JSON.stringify(accountUpdate), token);
		return response;
	}

	static async createAccount(token: string, accountCreate: AccountCreate): Promise<Response> {
		const response = await fast.post(`accounts`, JSON.stringify(accountCreate), token);
		return response;
	}

	static async getFiltersForUser(token: string, page: number): Promise<Response> {
		page = page - 1;
		const response = await fast.get(`filters?page=${page}`, token);
		return response;
	}

	static async deleteFilter(token: string, filterId: string): Promise<Response> {
		const response = await fast.delete(`filters/${filterId}`, token);
		return response;
	}

	static async updateFilter(token: string, filterId: string, filterUpdate: FilterUpdate): Promise<Response> {
		const response = await fast.put(`filters/${filterId}`, JSON.stringify(filterUpdate), token);
		return response;
	}

	static async createFilter(token: string, filterCreate: FilterCreate, categoryId: number): Promise<Response> {
		const response = await fast.post(`filters/category/${categoryId}`, JSON.stringify(filterCreate), token);
		return response;
	}

	static async getAllCategoriesForUser(token: string): Promise<Response> {
		const response = await fast.get('categories?limit=-1', token);
		return response;
	}

	static async getAllUsers(token: string, page: number): Promise<Response> {
		page = page - 1;
		const response = await fast.get(`admin/users?page=${page}`, token);
		return response;
	}

	static async deleteUser(token: string, userId: string): Promise<Response> {
		const response = await fast.delete(`admin/user/${userId}`, token);
		return response;
	}

	static async updateUserAsAdmin(token: string, userId: string, userUpdate: UserAdminUpdate): Promise<Response> {
		const response = await fast.put(`admin/user/${userId}`, JSON.stringify(userUpdate), token);
		return response;
	}

	static async getCategoriesForUser(token: string, page: number): Promise<Response> {
		page = page - 1;
		const response = await fast.get(`categories?page=${page}`, token);
		return response;
	}

	static async deleteCategory(token: string, categoryId: string): Promise<Response> {
		const response = await fast.delete(`categories/${categoryId}`, token);
		return response;
	}

	static async updateCategory(token: string, categoryId: string, categoryUpdate: CategoryUpdate): Promise<Response> {
		const response = await fast.put(`categories/${categoryId}`, JSON.stringify(categoryUpdate), token);
		return response;
	}

	static async createCategory(token: string, categoryCreate: CategoryCreate, budgetId: number): Promise<Response> {
		const response = await fast.post(`categories/budget/${budgetId}`, JSON.stringify(categoryCreate), token);
		return response;
	}
}

type UserUpdate = {
	email: string | null;
	full_name: string | null;
	password: string | null;
	passwordConfirm: string | null;
};

type UserAdminUpdate = {
	email: string | null;
	full_name: string | null;
	password: string | null;
	is_active: boolean | null;
};

type UserOrAdminCreate = {
	isAdmin: boolean;
	email: string;
	password: string;
	full_name: string;
};

type TransactionUpdate = {
	amount: number | null;
	date: string | null;
	desc: string | null;
};

type TransactionCreate = {
	amount: number;
	date: string;
	desc: string;
};

type AccountUpdate = {
	name: string | null;
	account_type: 'savings' | 'checking' | 'credit' | null;
};

type AccountCreate = {
	name: string;
	account_type: 'savings' | 'checking' | 'credit';
};

type FilterUpdate = {
	filter_by: string | null;
};

type FilterCreate = {
	filter_by: string;
};

type CategoryUpdate = {
	name: string | null;
	amount: number | null;
	desc: string | null;
};

type CategoryCreate = {
	name: string;
	amount: number;
	desc: string;
};

type BudgetUpdate = {
	name: string | null;
	amount: number | null;
};

type BudgetCreate = {
	name: string;
	amount: number;
};
