task :default => :test

task :test => ["test:all"]

namespace :test do

  # Usage:
  #   rake test:unit
  #   rake test:unit[test_file]
  #   rake test:unit[test_file,test_class,test_method]
  desc "run unit tests"
  task :unit, [:file_name, :class_name, :test_name] do |task, args|
    if args.file_name.nil?
      sh "python3 -m unittest discover tests/unit"
    elsif args.class_name.nil?
      sh "python3 -m unittest tests/unit/#{args.file_name}.py"
    else
      sh "python3 -m unittest tests.unit.#{args.file_name}.#{args.class_name}.#{args.test_name}"
    end
  end

  # Usage:
  #   rake test:integration
  #   rake test:integration[test_file]
  #   rake test:integration[test_file,test_class,test_method]
  desc "run integration tests"
  task :integration, [:file_name, :class_name, :test_name] do |task, args|
    if args.file_name.nil?
      sh "python3 -m unittest discover tests/integration"
    elsif args.class_name.nil?
      sh "python3 -m unittest tests/integration/#{args.file_name}.py"
    else
      sh "python3 -m unittest tests.integration.#{args.file_name}.#{args.class_name}.#{args.test_name}"
    end
  end

  task :all => [:unit, :integration]
end

task :clean do
  rm_rf "build"
  rm_rf "dist"
  rm_f "MANIFEST"
end

namespace :pypi do
  desc "Upload a new version to PyPI"
  task :upload => :clean do
    sh "python3 setup.py sdist bdist_wheel"
    sh "twine upload dist/*"
  end
end

namespace :lint do
  # We are only checking linting errors (for now),
  # so we use --disable to skip refactor(R), convention(C), and warning(W) messages
  desc "Evaluate test code quality using pylintrc file"
  task :tests do
    puts `pylint --disable=R,C,W tests --rcfile=.pylintrc --disable=R0801 --disable=W0232`
  end

  desc "Evaluate app code quality using pylintrc file"
  task :code do
    puts `pylint --disable=R,C,W braintree --rcfile=.pylintrc`
  end

  desc "Evaluate library code quality using pylintrc file"
  task :all do
    puts `pylint --disable=R,C,W braintree tests --rcfile=.pylintrc`
  end
end

task :lint => "lint:all"
