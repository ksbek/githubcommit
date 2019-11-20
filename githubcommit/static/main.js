define(['base/js/namespace','base/js/dialog','jquery'],function(IPython, dialog, $, mc){
    var callback = function(feedback_container, status, statusText) {
        var feedback = '';
        var container = $('#notebook-container');
        if (status == 500) {
            // display feedback to user
            feedback = '<div class="feedback '+feedback_container+' alert alert-danger alert-dismissible" role="alert"> \
                              <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
                              <div>'+statusText+'</div> \
                            </div>';

        } else {

            // display feedback to user
            feedback = '<div class="feedback '+feedback_container+' alert alert-success alert-dismissible" role="alert"> \
                              <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
                              '+statusText+' \
                               \
                            </div>';
        }

        // display feedback
        $('.feedback').remove();
        $('.' + feedback_container).remove();
        container.prepend(feedback);
    }

    var reg = /(.*?)\/notebooks/;
    var base_url = window.location.pathname.match(reg)[1];
    // we will define an action here that should happen when we ask to clear and restart the kernel.
    var git_add  = {
        help: 'Add current notebook',
        icon : 'fa-github',
        help_index : '',
        handler : function (env) {
            var on_success = undefined;
            var on_error = undefined;

            var div = $('<div/>')
            var p = $('<p/>').text("Add changes of this notebook to staging area.")

            div.append(p)

            // get the canvas for user feedback
            var container = $('#notebook-container');

            function on_ok(){
                var re = /\/notebooks(.*?)$/;
                var filepath = window.location.pathname.match(re)[1];
                var payload = {
                             'filename': filepath
                           };
                var settings = {
                    url : base_url + '/git/add',
                    processData : false,
                    type : "PUT",
                    dataType: "json",
                    data: JSON.stringify(payload),
                    contentType: 'application/json',
                    success: function(data) {
                        callback('add-feedback', data.status, data.statusText)
                    },
                    error: function(data) {
                        callback('add-feedback', 500, data.statusText)
                    }
                };

                // display preloader during add
                var preloader = '<img class="add-feedback" src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.5.8/ajax-loader.gif">';
                container.prepend(preloader);

                // add
                $.ajax(settings);
            }


            dialog.modal({
                body: div ,
                title: 'Add',
                buttons: {'Add':
                            { class:'btn-primary btn-large',
                              click:on_ok
                            },
                          'Cancel':{}
                    },
                notebook:env.notebook,
                keyboard_manager: env.notebook.keyboard_manager,
            })

        }
    };
    var git_commit  = {
        help: 'Commit current notebook and push to GitHub',
        icon : 'fa-github',
        help_index : '',
        handler : function (env) {
            var on_success = undefined;
            var on_error = undefined;

            var p = $('<p/>').text("Please enter your commit message.")
            var input = $('<textarea rows="4" cols="72"></textarea>')
            var div = $('<div/>')


            div.append(p)
               .append(input)

            // get the canvas for user feedback
            var container = $('#notebook-container');

            function on_ok(){
                var re = /\/notebooks(.*?)$/;
                var filepath = window.location.pathname.match(re)[1];
                var payload = {
                             'filename': filepath,
                             'msg': input.val()
                           };
                var settings = {
                    url : base_url + '/git/commit',
                    processData : false,
                    type : "PUT",
                    dataType: "json",
                    data: JSON.stringify(payload),
                    contentType: 'application/json',
                    success: function(data) {
                        callback('commit-feedback', data.status, data.statusText)
                    },
                    error: function(data) {
                        callback('commit-feedback', 500, data.statusText)
                    }
                };

                // display preloader during commit and push
                var preloader = '<img class="commit-feedback" src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.5.8/ajax-loader.gif">';
                container.prepend(preloader);

                // commit and push
                $.ajax(settings);
            }


            dialog.modal({
                body: div ,
                title: 'Commit',
                buttons: {'Commit':
                            { class:'btn-primary btn-large',
                              click:on_ok
                            },
                          'Cancel':{}
                    },
                notebook:env.notebook,
                keyboard_manager: env.notebook.keyboard_manager,
            })

        }
    };
    var git_push  = {
        help: 'Push current notebook to GitHub',
        icon : 'fa-github',
        help_index : '',
        handler : function (env) {
            var on_success = undefined;
            var on_error = undefined;

            var p = $('<p/>').text("Are you sure to push this notebook?")
            var div = $('<div/>')
            var checkbox = '<input type="checkbox" id="force_push"/><label>Force Push</label>'

            div.append(p);
            div.append(checkbox);

            // get the canvas for user feedback
            var container = $('#notebook-container');

            function on_ok(){
                var re = /\/notebooks(.*?)$/;
                var payload = {
                             'force': $("#force_push").prop('checked')
                           };
                var settings = {
                    url : base_url + '/git/push',
                    processData : false,
                    type : "PUT",
                    dataType: "json",
                    data: JSON.stringify(payload),
                    contentType: 'application/json',
                    success: function(data) {
                        callback('push-feedback', data.status, data.statusText)
                    },
                    error: function(data) {
                        callback('push-feedback', 500, data.statusText)
                    }
                };

                // display preloader during commit and push
                var preloader = '<img class="push-feedback" src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.5.8/ajax-loader.gif">';
                container.prepend(preloader);

                // commit and push
                $.ajax(settings);
            }


            dialog.modal({
                body: div ,
                title: 'Push Notebook',
                buttons: {'Push':
                            { class:'btn-primary btn-large',
                              click:on_ok
                            },
                          'Cancel':{}
                    },
                notebook:env.notebook,
                keyboard_manager: env.notebook.keyboard_manager,
            })

        }
    };
    var git_pull  = {
        help: 'Pull current notebook from GitHub',
        icon : 'fa-github',
        help_index : '',
        handler : function (env) {
            var on_success = undefined;
            var on_error = undefined;

            var p = $('<p/>').text("Are you sure to pull this notbook from github?")
            // var checkbox = '<input type="checkbox" id="force_pull"/><label>Force Pull</label>'
            var div = $('<div/>')

            div.append(p)
            // div.append(checkbox)

            // get the canvas for user feedback
            var container = $('#notebook-container');

            function on_ok(){
                var re = /\/notebooks(.*?)$/;
                var payload = {
                             // 'force': $("#force_pull").prop('checked')
                           };
                var settings = {
                    url : base_url + '/git/pull',
                    processData : false,
                    type : "POST",
                    dataType: "json",
                    data: JSON.stringify(payload),
                    contentType: 'application/json',
                    success: function(data) {
                        callback('pull-feedback', data.status, data.statusText)
                    },
                    error: function(data) {
                        callback('pull-feedback', 500, data.statusText)
                    }
                };

                // display preloader during commit and push
                var preloader = '<img class="pull-feedback" src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.5.8/ajax-loader.gif">';
                container.prepend(preloader);

                // commit and push
                $.ajax(settings);
            }


            dialog.modal({
                body: div ,
                title: 'Pull Notebook',
                buttons: {'Pull':
                            { class:'btn-primary btn-large',
                              click:on_ok
                            },
                          'Cancel':{}
                    },
                notebook:env.notebook,
                keyboard_manager: env.notebook.keyboard_manager,
            })

        }
    }

    function _on_load(){

        // log to console
        console.info('Loaded Jupyter extension: Git Commit and Push')

        // register new action
        var add = IPython.keyboard_manager.actions.register(git_add, 'add', 'jupyter-git')
        var commit = IPython.keyboard_manager.actions.register(git_commit, 'commit', 'jupyter-git')
        var push = IPython.keyboard_manager.actions.register(git_push, 'push', 'jupyter-git')
        var pull = IPython.keyboard_manager.actions.register(git_pull, 'pull', 'jupyter-git')

        // add button for new action
        IPython.toolbar.add_buttons_group([{'label': 'Add', 'action': add},
                                           {'label': 'Commit', 'action': commit},
                                           {'label': 'Push', 'action': push},
                                           {'label': 'Pull', 'action': pull}]);

    }

    return {load_ipython_extension: _on_load };
})
