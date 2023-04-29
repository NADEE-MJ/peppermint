<script lang="ts">
	export let userType: 'client' | 'admin' | 'public';

</script>

{#if userType === 'client'}
	 <nav class="list-nav p-4">
		 <ul>
			 <li><a href="/client/upload-csv-test">Upload CSV Test</a></li>
			 <li><a href="/client/accounts">Accounts</a></li>
			 <li><a href="/client/budget/mine">Budget</a></li>
			 <li><a href="/client/skelly">Skelly</a></li>
		 </ul>
	 </nav>
{:else if  userType === 'admin'}
	 <nav class="list-nav p-4">
		 <ul>
			 <li><a href="/admin/create">Create User / Admin</a></li>
			 <li><a href="/admin/delete">Delete User</a></li>
			 <li><a href="/admin/update">Update User</a></li>
			 <li><a href="/admin/find">Find User</a></li>
			 <li><a href="/admin/skelly">Skelly</a></li>
		 </ul>
	 </nav>
{/if}


