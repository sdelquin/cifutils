myapp = angular.module("myapp", ["ui.router", "ui.bootstrap", "angularFileUpload"])

StateConfig = ($stateProvider) ->
    $stateProvider
        .state "index"
            url: ""
            templateUrl: "/static/partials/index.html"
            abstract: true
        .state "index.landing"
            url: ""
            templateUrl: "/static/partials/index.landing.html"
        .state "index.menu"
            templateUrl: "/static/partials/index.menu.html"
            controller: MenuController
            abstract: true
        .state "index.menu.extract"
            url: "/extract"
            templateUrl: "/static/partials/index.menu.extract.html"
            controller: ExtractController
        .state "index.menu.extract.results"
            url: "/results"
            templateUrl: "/static/partials/index.menu.extract.results.html"

CSFRConfig = ($httpProvider) ->
    $httpProvider.defaults.xsrfCookieName = "csrftoken"
    $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken"

myapp.config(StateConfig)
myapp.config(CSFRConfig)

MenuController = ($scope, $state) ->
    $scope.$state = $state

ExtractController = ($scope, $upload, $http, $state) ->
    $scope.uploading = false
    $scope.select_files = ($files) ->
        $scope.selected_files = $files
    $scope.upload_files = () ->
        $scope.uploading = true
        $upload.upload
            url: "/api/extract/"
            file: $scope.selected_files[0]
        .success (data, status, headers, config) ->
            $scope.results = data
            $scope.uploading = false
            $state.transitionTo("index.menu.extract.results")
        .progress (evt) ->
            $scope.uploaded_percentage = parseInt(100.0 * evt.loaded / evt.total)
        .error (data) ->
            console.log(data)

