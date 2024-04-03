import React, { useState } from "react"
import axios from "axios"

function LoginPage() {
	const [username, setUsername] = useState("")
	const [password, setPassword] = useState("")

	const handleSubmit = async e => {
		e.preventDefault()
		try {
			const response = await axios.post("/login", { username, password })
			console.log(response.data)
		} catch (error) {
			console.error(error)
		}
	}

	return (
		<div>
			<form onSubmit={handleSubmit}>
				<label>
					Username:
					<input
						type="text"
						value={username}
						onChange={e => setUsername(e.target.value)}
					/>
				</label>
				<label>
					Password:
					<input
						type="password"
						value={password}
						onChange={e => setPassword(e.target.value)}
					/>
				</label>
				<input type="submit" value="Login" />
			</form>
		</div>
	)
}

export default LoginPage
