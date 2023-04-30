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

<div class="container p-10 mx-auto w-3/4">
	<form class="card p-4 grid grid-cols-2" action="?/createUserOrAdmin" method="POST" use:focusTrap={true} use:enhance={validateCreateUserOrAdmin}>

		<div>
			<header class="card-header text-center p-2">
				<strong class="text-7xl">Create new user or admin</strong>
			</header>

			<div class="p-6 space-y-4">
				<div class="space-y-4">
					<SlideToggle name="slider-label" bind:checked={isAdmin}>(Admin)</SlideToggle>
					<Textfield name="full_name" type="full_name" placeholder="Full Name" errorMessages={validationErrors?.name} />
					<Textfield name="email" type="email" placeholder="Email" errorMessages={validationErrors?.email} />
					<Textfield name="password" type="password" placeholder="Password" errorMessages={validationErrors?.password} />
					<Textfield name="passwordConfirm" type="password" placeholder="Confirm Password" errorMessages={validationErrors?.password} />
				</div>
				<div class="space-y-10">
					<div class="grid grid-cols-2">
						<button type="submit" class="btn btn-xl variant-filled-primary card-hover ">Create User/Admin</button>
					</div>
				</div>
			</div>
		</div>
	</form>
</div>
