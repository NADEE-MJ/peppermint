<script lang="ts">
	import { Avatar, popup, type PopupSettings } from '@skeletonlabs/skeleton';

	let AccountOptions: PopupSettings = {
		event: 'focus-click',
		target: 'accountOptions',
		placement: 'bottom'
	};

	export let userType: 'client' | 'admin' | 'public';

	const srcURL = () => {
		let seed: string;
		if (userType === 'client') {
			seed = 'Peppermint';
		} else if (userType === 'admin') {
			seed = 'admin';
		} else {
			seed = 'default';
		}

		return `https://api.dicebear.com/6.x/bottts-neutral/svg?seed=${seed}`;
	};

	const profileURL = `/${userType}/profile`;
</script>

<div>
	<button class="btn" use:popup={AccountOptions}>
		<Avatar src={srcURL()} width="w-10" background="bg-primary-500" />
	</button>
	<div class="card w-48 shadow-xl variant-filled-tertiary" data-popup="accountOptions">
		<div class="p-2 space-y-2">
			<nav class="list-nav">
				<ul>
					<li><a class="btn btn-md" href={profileURL}>Profile</a></li>
				</ul>
			</nav>
			<form action="/logout" method="POST" class="flex justify-center">
				<button class="btn btn-lg variant-filled-secondary">Logout</button>
			</form>
		</div>
		<div class="arrow variant-filled-tertiary absolute top-0" />
	</div>
</div>
