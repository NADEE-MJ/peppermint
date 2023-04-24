<script lang="ts">
	import { enhance, type SubmitFunction } from '$app/forms';
	import { toast } from '$lib/toasts';
	import Textfield from '$lib/components/Textfield.svelte';

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

<div class="container p-10 mx-auto w-2/5">
	<form class="card p-4" action="?/login" method="POST" use:enhance={validateLogin}>
		<header class="card-header text-center">
			<h1 class="text-xl">Peppermint</h1>
		</header>

		<div class="p-6">
			<div class="space-y-4">
				<Textfield name="email" type="email" placeholder="Email" errorMessages={validationErrors?.email} />
				<Textfield name="password" type="password" placeholder="Password" errorMessages={validationErrors?.password} />
			</div>
			<div class="grid grid-cols-3 p-2">
				<button type="submit" class="btn btn-xl variant-filled-primary card-hover col-start-2">Login</button>
				<a href="/signup" class="btn btn-md variant-filled-secondary card-hover mx-auto w-2/4 my-auto h-2/3">Signup</a>
			</div>
		</div>
	</form>
</div>
