<script lang="ts">
	import type { PageData } from './$types';
	import Profile from '$lib/components/Profile.svelte';

	export let data: PageData;
	const actionRoute = "?/updateUser";
</script>


<Profile data={data} {actionRoute} title="User Profile" />
