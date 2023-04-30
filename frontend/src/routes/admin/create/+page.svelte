<script lang="ts">
	import { enhance, type SubmitFunction } from '$app/forms';
	import { toast } from '$lib/toasts';
	import Textfield from '$lib/components/Textfield.svelte';
	import { focusTrap } from '@skeletonlabs/skeleton';
	import { SlideToggle } from '@skeletonlabs/skeleton';

	interface Errors {
		email: Array<string> | null;
		password: Array<string> | null;
		confirm_password: Array<string> | null;
		name: Array<string> | null;
	}

	let isAdmin: boolean = false;
	let validationErrors: Errors | null;

	const validateCreateUserOrAdmin: SubmitFunction = ({data}) => {
		data.append('isAdmin', isAdmin.toString());
		return async ({ result, update }) => {
			if (result.type === 'failure') {
				if (result.data) {
					const { errors, error, message } = result.data;
					if (errors) {
						validationErrors = errors;
					} else {
						validationErrors = null;
					}

					if (error) {
						toast.error(error);
					} else if (message) {
						toast.warning(message);
					}
				}
			}
			update({ reset: false });
		};
	};
</script>

<form class="card p-4 m-auto w-4/5" action="?/createUserOrAdmin" method="POST" use:focusTrap={true} use:enhance={validateCreateUserOrAdmin}>
	<div class="card-body">
		<header class="card-header text-center">
			<strong class="text-5xl">Create new user or admin</strong>
		</header>
		<div class="p-10">
			<div class="pt-5 grid grid-cols-2 gap-4">
				<div class="space-y-4">
					<Textfield name="email" label="Email" type="email" placeholder="Email" errorMessages={validationErrors?.email} />
					<Textfield name="full_name" label="Full Name" type="full_name" placeholder="Full Name" errorMessages={validationErrors?.name} />
				</div>
				<div class="space-y-4">
					<Textfield name="password" label="New Password" type="password" placeholder="Password" errorMessages={validationErrors?.password} />
					<Textfield name="passwordConfirm" label="Confirm New Password" type="password" placeholder="Confirm Password" errorMessages={validationErrors?.password} />
				</div>
				<div class="space-y-10">
			</div>
		</div>
		<div class="grid grid-cols-3">
			<div>
				<SlideToggle name="slider-label" bind:checked={isAdmin}>(Admin)</SlideToggle></div>
			<button type="submit" class="btn btn-lg variant-filled-primary card-hover ">Create</button>
			<div></div>
		</div>
	</div>
</form>
