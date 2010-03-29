load File.dirname(__FILE__) + "/cruise.rake"

task :default => :test

task :test do
  sh "nosetests"
end

task :clean do
  rm_rf "build"
  rm_rf "dist"
  rm_f "MANIFEST"
end

namespace :pypi do
  desc "Register the package with PyPI"
  task :register => :clean do
    sh "python setup.py register"
  end

  desc "Upload a new version to PyPI"
  task :upload => :clean do
    sh "python setup.py sdist upload"
  end
end

namespace :docs do
  desc "Generate docs"
  task :generate => "docs:clean" do
    Dir.chdir("docs") do
      sh "make html"
    end
  end

  desc "Clean docs"
  task :clean do
    Dir.chdir("docs") do
      sh "make clean"
    end
  end
end
