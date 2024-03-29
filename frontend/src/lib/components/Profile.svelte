<script lang="ts">
	import { enhance, type SubmitFunction } from '$app/forms';
	import Textfield from '$lib/components/Textfield.svelte';
	import { toast } from '$lib/toasts';
	import { focusTrap } from '@skeletonlabs/skeleton';

	export let actionRoute: string;
	export let title: string;
	export let data: { email?: undefined; full_name?: undefined } | { email: string; full_name: string };

	type UserFormData = {
		email?: string | null;
		password?: string | null;
		passwordConfirm?: string | null;
		full_name?: string | null;
	};

	let userFormData: UserFormData = {
		email: data.email,
		password: null,
		passwordConfirm: null,
		full_name: data.full_name
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
			} else {
				validationErrors = null;
			}
			update({ reset: false });
		};
	};
</script>

<form class="card p-4 m-auto w-4/5" method="POST" action={actionRoute} use:focusTrap={true} use:enhance={validateUpdateUser}>
	<header class="card-header text-center">
		<strong class="text-5xl">{title}</strong>
	</header>

	<div class="p-10">
		<div class="grid grid-cols-2 gap-4">
			<div class="space-y-4">
				<Textfield label="Email" name="email" type="email" placeholder="Email" errorMessages={validationErrors?.email} value={userFormData.email} />
				<Textfield
					label="Full Name"
					name="full_name"
					type="text"
					placeholder="Full Name"
					errorMessages={validationErrors?.full_name}
					value={userFormData.full_name}
				/>
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
		<div class="grid grid-cols-3 mt-6">
			<div />
			<button type="submit" class="btn btn-lg variant-filled-primary card-hover">Update Profile</button>
			<div />
		</div>
	</div>
</form>
