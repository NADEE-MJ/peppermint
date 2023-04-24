<script lang="ts">
	import { enhance, type SubmitFunction } from '$app/forms';
	import { toast } from '$lib/toasts';
	import Textfield from '$lib/components/Textfield.svelte';

	interface Errors {
		email: Array<string> | null;
		password: Array<string> | null;
		confirm_password: Array<string> | null;
		name: Array<string> | null;
	}

	let validationErrors: Errors | null;

	const validateSignup: SubmitFunction = () => {
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
						toast.error(message);
					}
				}
			}
			update({ reset: false });
		};
	};
</script>

<div class="container p-10 mx-auto w-2/5">
	<form class="card p-4" action="?/signup" method="POST" use:enhance={validateSignup}>
		<header class="card-header text-center p-2">
			<h1 class="text-xl">Sign Up</h1>
		</header>

		<div class="p-6">
			<div class="space-y-4">
				<Textfield name="full_name" type="full_name" placeholder="Full Name" errorMessages={validationErrors?.name} />
				<Textfield name="email" type="email" placeholder="Email" errorMessages={validationErrors?.email} />
				<Textfield name="password" type="password" placeholder="Password" errorMessages={validationErrors?.password} />
				<Textfield name="passwordConfirm" type="password" placeholder="Confirm Password" errorMessages={validationErrors?.password} />
			</div>
			<div class="grid grid-cols-3 p-2">
				<div/>
				<button type="submit" class="btn btn-xl variant-filled-primary card-hover">Signup</button>
			</div>
		</div>
	</form>
</div>
