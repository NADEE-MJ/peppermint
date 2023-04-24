<script lang="ts">
	import { enhance, type SubmitFunction } from '$app/forms';
	import type { PageData } from './$types';
	import Textfield from '$lib/components/Textfield.svelte';
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

<form class="card p-4" method="POST" action="?/updateUser" use:enhance={validateUpdateUser}>
	<header class="card-header text-center">
		<h1 class="text-xl">User Profile</h1>
	</header>

	<div class="p-6 space-y-4">
		<div class="grid grid-cols-2 gap-4">
			<div class="space-y-4">
				<Textfield label="Email" name="email" type="email" placeholder="Email" errorMessages={validationErrors?.email} value={userFormData.email} />
				<Textfield label="Full Name" name="full_name" type="text" placeholder="Full Name" errorMessages={validationErrors?.full_name} value={userFormData.full_name} />
			</div>
			<div class="space-y-4">
				<Textfield
					label="New Password"
					name="password"
					type="password"
					placeholder="New Password"
					errorMessages={validationErrors?.password}
					value={userFormData.password}
				/>
				<Textfield
					label="Confirm New Password"
					name="passwordConfirm"
					type="password"
					placeholder="Confirm New Password"
					errorMessages={validationErrors?.passwordConfirm}
					value={userFormData.passwordConfirm}
				/>
			</div>
		</div>
		<div class="grid grid-cols-3 gap-10">
			<button type="submit" class="btn btn-xl col-start-2 variant-filled-primary card-hover">Update Account Info</button>
		</div>
	</div>
</form>
