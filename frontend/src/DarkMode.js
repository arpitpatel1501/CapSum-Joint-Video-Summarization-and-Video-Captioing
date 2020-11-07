import React, { useEffect } from 'react';

function DarkMode(){
	//console.log(props)
	const SwitchMode=()=>{
		if (document.body.classList.contains('dark')) {
			document.body.classList.remove('dark')
			localStorage.setItem("darkMode", false);
		}
		else {
			document.body.classList.add('dark');
			localStorage.setItem("darkMode", true);
		}
	}
	const onLoad=()=>{
		if(localStorage.getItem("darkMode")==='true'){
			SwitchMode()
		}
		else{
			document.getElementById("dark-mode-switch").checked = true;
		}
	}
	useEffect(() => {
		onLoad()
	});

	return(
		<div className="dark-toggle" style={{marginTop:'10px',paddingRight:'5vw'}} >
			<input type="checkbox" onClick={SwitchMode} id="dark-mode-switch" name="checkbox" className="switch" />
		</div>
	)
	
  }
  export default DarkMode;
  