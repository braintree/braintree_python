task :default => :test

task :test => ["test:all"]

namespace :test do

  # Usage:
  #   rake test:unit
  #   rake test:unit[test_configuration]
  #   rake test:unit[test_configuration,test_base_merchant_path_for_development]
  desc "run unit tests"
  task :unit, [:file_name, :test_name] do |task, args|
    if args.file_name.nil?
      sh "nosetests tests/unit"
    elsif args.test_name.nil?
      sh "nosetests tests/unit/#{args.file_name}.py"
    else
      sh "nosetests tests/unit/#{args.file_name}.py -m #{args.test_name}"
    end
  end

  # Usage:
  #   rake test:integration
  #   rake test:integration[test_plan]
  #   rake test:integration[test_plan,test_all_returns_all_the_plans]
  desc "run integration tests"
  task :integration, [:file_name, :test_name] do |task, args|
    if args.file_name.nil?
      sh "nosetests tests/integration"
    elsif args.test_name.nil?
      sh "nosetests tests/integration/#{args.file_name}.py"
    else
      sh "nosetests tests/integration/#{args.file_name}.py -m #{args.test_name}"
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
