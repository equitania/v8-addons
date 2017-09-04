openerp.web_tinymce = function(instance)
{
    instance.web.form.widgets.add('text_html',
            'instance.web_tinymce.FieldTinyMceEditor');
    instance.web.form.widgets.add('html',
            'instance.web_tinymce.FieldTinyMceEditor');
    instance.web.form.widgets.add('ourNewEditor',
            'instance.web_tinymce.FieldTinyMceEditor');

    instance.web_tinymce.FieldTinyMceEditor = instance.web.form.FieldText.extend({
	    init: function() {
	        this._super.apply(this, arguments);
	    },
	    initialize_content: function() {
	        var self = this;
	        if (! this.get("effective_readonly")) {
	            self._updating_editor = false;
	            this.$textarea = this.$el.find('textarea');
	            var width = ((this.node.attrs || {}).editor_width || 'calc(100% - 4px)');
	            var height = ((this.node.attrs || {}).editor_height || 250);
	            this.$el.find('textarea').attr("id", self.name);
	        }
	    },
	    focus: function() {
	        var input = !this.get("effective_readonly") && this.$cleditor
	        return input ? input.focus() : false;
	    },
	    store_dom_value: function(){
	    	for (inst in tinyMCE.editors) {
	    	    if (tinyMCE.editors[inst].getContent){
	    	    	if(tinyMCE.editors[inst].id == this.name){
	    	    		this.internal_set_value(tinyMCE.editors[inst].getContent());
	    	    	}
	    	    }
	    	}
	    },
	    render_value: function() {
	        if (! this.get("effective_readonly")) {
	            this.$textarea.val(this.get('value') || '');
	            this._updating_editor = true;
	            var self = this;

	            // EQ: Lösung für unser Problem mit dem Dialog "Sende eine Email" --> gemacht von Paul ! :-)
				for (var i = 0; i < tinyMCE.editors.length; i++) {
					if(tinyMCE.editors[i].id == this.name){
							tinyMCE.editors[i].destroy();
						}
				}

	            //tinymce.remove();
	            tinymce.init({
	            	selector: "#"+self.name ,
	            	relative_urls: false,
	            	remove_script_host: false,
	            	plugins : 'advlist lists charmap print preview fullpage hr compat3x colorpicker  emoticons  table code',
		            setup: function (editor) {
		            	for (var i = 0; i < editor.length; i++) {
			            	editor[i].onInit.add(function(editor) {
			                    this.setContent(self.get('value') || '', {format: 'raw'});
			                });
		            	}
		            }
	            });

	        } else {
	            this.$el.html(this.get('value'));
	            //tinymce.remove()
	        }
	    },
    });
    instance.web_tinymce.FieldTinyMceEditorRaw = instance.web_tinymce.FieldTinyMceEditor.extend({
        filter_html: function(value){
            return value;
        }
    });
}