/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors');
module.exports = {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {
			colors: {
				impo: colors.violet[400],
				expo: colors.amber[400],
				balance: colors.blue[400],

			}
		},
	},
	plugins: [],
}
