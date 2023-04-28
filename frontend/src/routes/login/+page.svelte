<script lang="ts">
	import { enhance, type SubmitFunction } from '$app/forms';
	import Textfield from '$lib/components/Textfield.svelte';
	import { focusTrap, modalStore, type ModalSettings } from '@skeletonlabs/skeleton';
	import { toast } from '$lib/toasts';

	const sendMagicLink: ModalSettings = {
		type: 'prompt',
		title: 'Get a Magic Link 🪄',
		body: 'This will send a one-time login link to your email address to log you in to your account. From there you may change your password on your account page.',
		value: 'Email',
		valueAttr: { type: 'email', minlength: 3, maxlength: 30, required: true },
		response: async (email: string) => {
			const res = await fetch(`magic-link?email=${email}`, { method: 'POST' });
			const data = await res.json();
			if (data?.success) {
				toast.success('Magic Link sent! 🪄');
			} else if (data?.message !== 'No email provided') {
				toast.error(data.message);
			}
		}
	};

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
						toast.warning(message);
					}
				}
			}
			update({ reset: false });
		};
	};
</script>

<div class="container p-10 mx-auto w-3/4">
	<form class="card p-4 grid grid-cols-2" action="?/login" method="POST" use:focusTrap={true} use:enhance={validateLogin}>
		<div>
			<div class="mx-auto">
				<img src="https://tecdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp" alt="Login Left" />
			</div>
		</div>
		<div>
			<header class="card-header text-center">
				<strong class="text-7xl">Login</strong>
			</header>

			<div class="p-6 space-y-4">
				<div class="space-y-4">
					<Textfield name="email" type="email" placeholder="Email" errorMessages={validationErrors?.email} />
					<Textfield name="password" type="password" placeholder="Password" errorMessages={validationErrors?.password} />
				</div>
				<div class="space-y-10">
					<div class="grid grid-cols-2">
						<button type="submit" class="btn btn-xl w-3/5 variant-filled-primary card-hover">Login</button>
						<button type="button" class="justify-self-end" on:click={() => modalStore.trigger(sendMagicLink)}>Forgot password?</button>
					</div>
					<p class="font-semibold">
						Don't have an account?
						<a href="/signup">Register</a>
					</p>
				</div>
			</div>
		</div>
	</form>
</div>
