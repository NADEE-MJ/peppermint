<script lang="ts">
	import { enhance, type SubmitFunction } from '$app/forms';
	import type { PageData } from './$types';
	import Textfield from '$lib/components/textfield.svelte';
	import { toast } from '$lib/toasts';

	type UserFormData = {
		email?: string | null;
		password?: string | null;
		passwordConfirm?: string | null;
		full_name?: string | null;
	};

	export let data: PageData;
	let userFormData: UserFormData = {
		email: data.userRecord.email,
		password: null,
		passwordConfirm: null,
		full_name: data.userRecord.full_name
	};

	interface Errors {
		email: Array<string> | null;
		password: Array<string> | null;
		passwordConfirm: Array<string> | null;
		full_name: Array<string> | null;
	}

	let validationErrors: Errors | null;

	const validateUpdateUser: SubmitFunction = () => {
		return async ({ result, update }) => {
			if (result.type === 'failure') {
				if (result.data) {
					const { errors, message } = result.data;
					if (errors) {
						validationErrors = errors;
					} else {
						validationErrors = null;
					}
					if (message) {
						toast.error(message);
					}
				}
			}
			update({ reset: false });
		};
	};
</script>

<div class="page-container">
	<form class="card p-4" method="POST" action="?/updateUser" use:enhance={validateUpdateUser}>
		<header class="card-header text-center p-2">
			<h2>User Profile</h2>
		</header>

		<div class="p-6 grid gap-4">
			<div class="space-y-4">
				<Textfield name="email" type="email" placeholder="Email" errorMessages={validationErrors?.email} value={userFormData.email} />
				<Textfield
					name="password"
					type="password"
					placeholder="New Password"
					errorMessages={validationErrors?.password}
					value={userFormData.password}
				/>
				<Textfield
					name="passwordConfirm"
					type="password"
					placeholder="Confirm New Password"
					errorMessages={validationErrors?.passwordConfirm}
					value={userFormData.passwordConfirm}
				/>
				<Textfield name="full_name" type="text" placeholder="Full Name" errorMessages={validationErrors?.full_name} value={userFormData.full_name} />
			</div>
			<div class="flex justify-center">
				<button type="submit" class="btn variant-filled btn-xl">Update Account Info</button>
			</div>
		</div>
	</form>
</div>
