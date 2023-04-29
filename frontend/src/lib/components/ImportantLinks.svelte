<script lang="ts">
	import Documents from '$lib/assets/Documents.svg.svelte';
	import Github from '$lib/assets/Github.svg.svelte';
</script>

<div class="grid grid-cols-3">
	<div class="col-start-2 mx-auto">
		<a class="btn btn-md card-hover variant-filled-tertiary w-2/5" href="https://github.com/NADEE-MJ/peppermint">
			<Github classOverride="w-10 h-" />
		</a>
		<a
			class="btn btn-md card-hover variant-filled-tertiary w-2/5"
			href="https://docs.google.com/document/d/1bKWnTiJezL7QpqsS6EcR1HyTvwvQB3s1RVC6jnCUPJ4"
		>
			<Documents classOverride="w-10 h-6" />
		</a>
	</div>
</div>
