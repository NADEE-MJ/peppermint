<script lang="ts">
	import { enhance, type SubmitFunction } from '$app/forms';
	import { toast } from '$lib/toasts';
	import Textfield from '$lib/components/Textfield.svelte';
	import { focusTrap } from '@skeletonlabs/skeleton';

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

<div class="container p-10 mx-auto w-3/4">
	<form class="card p-4 grid grid-cols-2" action="?/signup" method="POST" use:focusTrap={true} use:enhance={validateSignup}>
		<div>
			<div class="mx-auto">
				<img src="https://tecdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp" alt="Login Left" />
		  	</div>
		</div>

		<div>
			<header class="card-header text-center p-2">
				<strong class="text-7xl">Register</strong>
			</header>

			<div class="p-6 space-y-4">
				<div class="space-y-4">
					<Textfield name="full_name" type="full_name" placeholder="Full Name" errorMessages={validationErrors?.name} />
					<Textfield name="email" type="email" placeholder="Email" errorMessages={validationErrors?.email} />
					<Textfield name="password" type="password" placeholder="Password" errorMessages={validationErrors?.password} />
					<Textfield name="passwordConfirm" type="password" placeholder="Confirm Password" errorMessages={validationErrors?.password} />
				</div>
				<div class="space-y-10">
					<div class="grid grid-cols-2">
						<button type="submit" class="btn btn-xl variant-filled-primary card-hover w-3/5">Signup</button>
					</div>
					<p class="font-semibold">
						Already have an account?
						<a href="/login">Login</a>
					</p>
				</div>

			</div>
		</div>
	</form>
</div>
