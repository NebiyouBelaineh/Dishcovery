const tags = document.querySelector("#tagsContent");
const cursor_tag = document.querySelector("#showTags");
cursor_tag.addEventListener("click", function(e){
	if(this.children[0].getAttribute("name") === "chevron-up-outline"){
		this.children[0].setAttribute("name", "chevron-down-outline")
	}else{
		this.children[0].setAttribute("name", "chevron-up-outline")

	}
})
$("#tagsContent").hide();
$("#showTags").click(function(){
	$("#tagsContent").slideToggle(300);
  });
