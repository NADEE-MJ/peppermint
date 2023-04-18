<script lang="ts">
	import { enhance, type SubmitFunction } from '$app/forms';
	import { toast } from '$lib/toasts';
	import Textfield from '$lib/components/textfield.svelte';

	interface Errors {
		email: Array<string> | null;
		password: Array<string> | null;
	}

	let validationErrors: Errors | null;

	const validateLogin: SubmitFunction = () => {
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



<div class="page-container">
	<form action="?/login" method="POST" use:enhance={validateLogin}>
		<div class="card p-4">
			<header class="card-header text-center p-2">
				<h2>Login</h2>
			</header>

			<div class="p-6 ">
				<div class="space-y-4">
					<Textfield name="email" type="email" placeholder="Email" errorMessages={validationErrors?.email} />
					<Textfield name="password" type="password" placeholder="Password" errorMessages={validationErrors?.password} />
				</div>
				<div class="flex justify-center p-2">
					<button type="submit" class="btn btn-filled-primary btn-xl">Login</button>
					<a href="/signup" class="btn btn-filled-primary btn-xl">Signup</a>
				</div>
			</div>
		</div>
	</form>
</div>

